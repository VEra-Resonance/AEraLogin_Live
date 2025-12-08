"""
VEra-Resonance — Blockchain Sync Module
© 2025 Karlheinz Beismann — VEra-Resonance Project
Licensed under the Apache License, Version 2.0

Background service to sync scores from database to blockchain
"""

import asyncio
import sqlite3
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from logger import setup_logger
from web3_service import web3_service

logger = setup_logger(__name__)

# Global sync queue
sync_queue = asyncio.Queue()
_sync_processor_task = None
_is_running = False

# Sync configuration
RETRY_DELAY_SECONDS = 300  # 5 minutes between retries
MAX_RETRIES = 3


async def sync_score_after_update(address: str, score: int, conn: Optional[sqlite3.Connection] = None):
    """
    Sync Resonance Score to blockchain after database update
    
    Resonance = Own Score + Avg Follower Score
    Only syncs at milestones (every 2 points: 50, 52, 54, 56, 58, 60...)
    
    Args:
        address: User wallet address
        score: User's own score (from DB)
        conn: Optional database connection (for transaction context)
    """
    try:
        from resonance_calculator import calculate_resonance_score
        
        # Calculate total resonance (own + avg follower)
        if conn:
            try:
                own, avg_follower, count, total_resonance = calculate_resonance_score(address, conn)
                logger.info(f"📊 Resonance for {address[:10]}: {own} (own) + {avg_follower} (avg follower) = {total_resonance}")
            except Exception as e:
                logger.warning(f"⚠️ Resonance calculator error, using own score: {e}")
                total_resonance = score
        else:
            # Fallback: use own score only if no connection
            total_resonance = score
            logger.warning(f"⚠️ No DB connection - using own score only: {score}")
        
        # Sync at every 2-point milestone (50, 52, 54, 56, 58, 60...)
        # OR sync if this is the first sync (blockchain_score is still 0)
        if total_resonance % 2 != 0:
            logger.debug(f"⏸️ Skipping blockchain sync for {address}: {total_resonance} is not a 2-point milestone")
            return
        
        logger.info(f"📊 Syncing milestone resonance to blockchain: {address} → {total_resonance}")
        
        # Update resonance score on blockchain
        success, result = await web3_service.update_blockchain_score(address, total_resonance)
        
        if success:
            logger.info(f"✅ Score synced to blockchain: {result.get('tx_hash')}")
            
            # Update sync status in database if connection provided
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET last_blockchain_sync = CURRENT_TIMESTAMP
                    WHERE address = ?
                """, (address.lower(),))
                conn.commit()
                logger.info(f"✅ Database sync status updated for {address}")
        else:
            logger.error(f"❌ Failed to sync score to blockchain: {result.get('error')}")
            # Database timestamp will remain unchanged (indicates sync failure)
                
    except Exception as e:
        logger.error(f"❌ Error syncing score for {address}: {e}")
        # Database timestamp will remain unchanged (indicates sync failure)


async def should_sync_score(address: str, db_score: int, conn: sqlite3.Connection) -> bool:
    """
    Check if score should be synced to blockchain
    
    Args:
        address: User wallet address
        db_score: Current score in database
        conn: Database connection
        
    Returns:
        True if sync is needed, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT last_blockchain_sync
            FROM users
            WHERE address = ?
        """, (address.lower(),))
        
        row = cursor.fetchone()
        if not row:
            return True  # No sync record, sync needed
        
        last_sync = row[0]
        
        # Check if enough time has passed since last sync
        if last_sync:
            last_sync_time = datetime.fromisoformat(last_sync)
            if datetime.now() - last_sync_time < timedelta(minutes=5):
                return False  # Too soon to sync again
        
        # Get blockchain score to compare
        blockchain_score = await web3_service.get_blockchain_score(address)
        
        # Sync if scores differ
        return db_score != blockchain_score
        
    except Exception as e:
        logger.error(f"Error checking if sync needed for {address}: {e}")
        return True  # On error, try to sync


async def add_to_sync_queue(address: str, score: int):
    """
    Add address/score pair to sync queue for background processing
    
    Args:
        address: User wallet address
        score: Score to sync
    """
    try:
        await sync_queue.put({
            "address": address,
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "retries": 0
        })
        logger.info(f"📋 Added to sync queue: {address} → {score}")
    except Exception as e:
        logger.error(f"Error adding {address} to sync queue: {e}")


async def process_sync_queue():
    """
    Background task to process score sync queue
    """
    global _is_running
    _is_running = True
    
    logger.info("🔄 Score sync queue processor started")
    
    while _is_running:
        try:
            # Get next item from queue (wait up to 10 seconds)
            try:
                item = await asyncio.wait_for(sync_queue.get(), timeout=10.0)
            except asyncio.TimeoutError:
                continue  # No items, continue loop
            
            address = item["address"]
            score = item["score"]
            retries = item.get("retries", 0)
            
            logger.info(f"📊 Processing sync queue item: {address} → {score} (attempt {retries + 1})")
            
            # Attempt sync
            success, result = await web3_service.update_blockchain_score(address, score)
            
            if success:
                logger.info(f"✅ Sync successful: {result.get('tx_hash')}")
                
                # Update database blockchain_score and sync timestamp
                try:
                    import sqlite3
                    import os
                    DB_PATH = os.path.join(os.path.dirname(__file__), "aera.db")
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET blockchain_score = ?,
                            last_blockchain_sync = CURRENT_TIMESTAMP
                        WHERE address = ?
                    """, (score, address.lower()))
                    conn.commit()
                    conn.close()
                    logger.info(f"✅ Database updated: blockchain_score={score} for {address[:10]}...")
                except Exception as db_error:
                    logger.error(f"❌ Failed to update database for {address}: {db_error}")
            else:
                logger.error(f"❌ Sync failed: {result.get('error')}")
                
                # Retry logic
                if retries < MAX_RETRIES:
                    item["retries"] = retries + 1
                    # Re-add to queue after delay
                    await asyncio.sleep(RETRY_DELAY_SECONDS)
                    await sync_queue.put(item)
                    logger.info(f"♻️ Re-queued for retry: {address}")
                else:
                    logger.error(f"❌ Max retries reached for {address}, giving up")
            
            # Mark task as done
            sync_queue.task_done()
            
        except Exception as e:
            logger.error(f"Error processing sync queue: {e}")
            await asyncio.sleep(1)  # Brief pause on error
    
    logger.info("🛑 Score sync queue processor stopped")


async def start_sync_queue_processor():
    """
    Start the background sync queue processor
    """
    global _sync_processor_task, _is_running
    
    if _sync_processor_task is not None and not _sync_processor_task.done():
        logger.warning("⚠️ Sync queue processor already running")
        return
    
    _is_running = True
    _sync_processor_task = asyncio.create_task(process_sync_queue())
    logger.info("✅ Sync queue processor started")


async def stop_sync_queue_processor():
    """
    Stop the background sync queue processor
    """
    global _sync_processor_task, _is_running
    
    _is_running = False
    
    if _sync_processor_task:
        _sync_processor_task.cancel()
        try:
            await _sync_processor_task
        except asyncio.CancelledError:
            pass
        
        logger.info("✅ Sync queue processor stopped")
