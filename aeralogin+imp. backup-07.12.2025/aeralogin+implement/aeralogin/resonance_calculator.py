"""
Resonance Score Calculation Module

Resonance = Own Score + Average Follower Score

This creates a network effect where creators with engaged followers
have higher resonance on the blockchain.
"""
import sqlite3
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

def calculate_resonance_score(address: str, conn: sqlite3.Connection) -> Tuple[int, int, int, int]:
    """
    Calculate total resonance score for a creator
    
    Formula: Resonance = Own Score + Avg Follower Score
    
    Args:
        address: User wallet address
        conn: Database connection
        
    Returns:
        (own_score, avg_follower_score, follower_count, total_resonance)
    """
    try:
        address = address.lower()
        cursor = conn.cursor()
        
        # Get own score (pending_bonus is only for DB rewards, not blockchain sync!)
        cursor.execute("SELECT score FROM users WHERE address=?", (address,))
        user = cursor.fetchone()
        own_score = user[0] if user else 0
        
        # Get follower stats
        cursor.execute("""
            SELECT COUNT(*) as count, AVG(follower_score) as avg_score
            FROM followers 
            WHERE owner_wallet=?
        """, (address,))
        
        stats = cursor.fetchone()
        follower_count = stats[0] or 0
        avg_follower_score = int(stats[1] or 0)
        
        # Resonance Formula: Own Score + Avg Follower Score (no pending_bonus for blockchain!)
        total_resonance = own_score + avg_follower_score
        
        logger.info(f"📊 Resonance for {address[:10]}: {own_score} + {avg_follower_score} = {total_resonance} ({follower_count} followers)")
        
        return own_score, avg_follower_score, follower_count, total_resonance
        
    except Exception as e:
        logger.error(f"Error calculating resonance for {address}: {e}")
        return 0, 0, 0, 0


def should_sync_resonance(address: str, conn: sqlite3.Connection) -> Tuple[bool, int]:
    """
    Check if resonance score should be synced to blockchain
    
    Args:
        address: User wallet address
        conn: Database connection
        
    Returns:
        (should_sync: bool, target_score: int)
    """
    try:
        # Calculate current resonance
        own, avg_follower, count, total_resonance = calculate_resonance_score(address, conn)
        
        # Sync at every point change (milestone = 1)
        if total_resonance % 1 != 0:
            logger.debug(f"⏸️ Skipping sync for {address[:10]}: {total_resonance} is not a milestone")
            return False, total_resonance
        
        # Check if blockchain score matches
        from web3_service import web3_service
        import asyncio
        
        try:
            blockchain_score = asyncio.run(web3_service.get_blockchain_score(address))
            
            if blockchain_score == total_resonance:
                logger.debug(f"✅ Already synced for {address[:10]}: {total_resonance}")
                return False, total_resonance
            
            logger.info(f"🔄 Sync needed for {address[:10]}: {blockchain_score} → {total_resonance}")
            return True, total_resonance
            
        except Exception as e:
            logger.error(f"Error checking blockchain score: {e}")
            return False, total_resonance
            
    except Exception as e:
        logger.error(f"Error in should_sync_resonance: {e}")
        return False, 0
