"""
🤖 Telegram Bot Service für ECHTE Einmal-Links
=============================================

Nutzt die Telegram Bot API um Invite Links mit member_limit=1 zu erstellen.
Jeder Link kann NUR von EINER Person genutzt werden!

Voraussetzungen:
1. Bot von @BotFather erstellen
2. Bot als Admin zur Gruppe hinzufügen (mit Invite-Rechten)
3. TELEGRAM_BOT_TOKEN und TELEGRAM_GROUP_ID in .env setzen

Author: VEra-Resonance
Created: 2025-12-09
"""

import os
import aiohttp
import logging
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any

# Logger
logger = logging.getLogger("TelegramBot")
logger.setLevel(logging.INFO)

# Telegram Bot API Base URL
TELEGRAM_API_BASE = "https://api.telegram.org/bot"


class TelegramBotService:
    """
    Service für Telegram Bot API Interaktionen
    """
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.default_group_id = os.getenv("TELEGRAM_GROUP_ID", "")
        self._bot_info = None
    
    @property
    def is_configured(self) -> bool:
        """Prüft ob Bot konfiguriert ist"""
        return bool(self.bot_token and self.default_group_id)
    
    @property
    def api_url(self) -> str:
        """Telegram Bot API URL"""
        return f"{TELEGRAM_API_BASE}{self.bot_token}"
    
    async def _api_request(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generischer Telegram API Request
        
        Args:
            method: API Methode (z.B. "getMe", "createChatInviteLink")
            params: Parameter für den Request
        
        Returns:
            API Response als Dict
        """
        url = f"{self.api_url}/{method}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=params or {}) as response:
                    result = await response.json()
                    
                    if not result.get("ok"):
                        error_desc = result.get("description", "Unknown error")
                        logger.error(f"❌ Telegram API Error: {error_desc}")
                        return {"ok": False, "error": error_desc}
                    
                    return result
                    
        except aiohttp.ClientError as e:
            logger.error(f"❌ Telegram API Connection Error: {str(e)}")
            return {"ok": False, "error": f"Connection error: {str(e)}"}
        except Exception as e:
            logger.error(f"❌ Telegram API Exception: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    async def get_bot_info(self) -> Dict[str, Any]:
        """
        Holt Bot-Informationen (getMe)
        
        Returns:
            Bot Info oder Error
        """
        if self._bot_info:
            return {"ok": True, "result": self._bot_info}
        
        result = await self._api_request("getMe")
        
        if result.get("ok"):
            self._bot_info = result.get("result", {})
            logger.info(f"🤖 Bot Info: @{self._bot_info.get('username')}")
        
        return result
    
    async def verify_bot_permissions(self, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Prüft ob Bot Admin-Rechte in der Gruppe hat
        
        Args:
            chat_id: Telegram Chat/Group ID (optional, nutzt default)
        
        Returns:
            {"ok": True, "can_invite": True} oder Error
        """
        target_chat = chat_id or self.default_group_id
        
        if not target_chat:
            return {"ok": False, "error": "No group ID configured"}
        
        # Get bot's own info first
        bot_info = await self.get_bot_info()
        if not bot_info.get("ok"):
            return bot_info
        
        bot_id = self._bot_info.get("id")
        
        # Get chat member info for the bot
        result = await self._api_request("getChatMember", {
            "chat_id": target_chat,
            "user_id": bot_id
        })
        
        if not result.get("ok"):
            return result
        
        member = result.get("result", {})
        status = member.get("status", "")
        
        # Check if admin with invite rights
        if status in ["creator", "administrator"]:
            can_invite = member.get("can_invite_users", False)
            return {
                "ok": True,
                "status": status,
                "can_invite": can_invite,
                "message": "✅ Bot has invite permissions" if can_invite else "❌ Bot lacks invite permissions"
            }
        else:
            return {
                "ok": False,
                "status": status,
                "can_invite": False,
                "error": f"Bot is not admin (status: {status})"
            }
    
    async def create_one_time_invite(
        self,
        chat_id: Optional[str] = None,
        name: Optional[str] = None,
        expire_seconds: int = 300
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        🎟️ Erstellt einen EINMAL-LINK (member_limit=1)
        
        Der Link kann NUR von EINER Person verwendet werden!
        
        Args:
            chat_id: Telegram Group/Chat ID (optional, nutzt default)
            name: Name für den Link (z.B. "0x1234...")
            expire_seconds: Gültigkeit in Sekunden (default: 5 Minuten)
        
        Returns:
            (success: bool, result: Dict)
            result enthält bei Erfolg: invite_link, name, expire_date, member_limit
        """
        target_chat = chat_id or self.default_group_id
        
        if not self.bot_token:
            return False, {"error": "TELEGRAM_BOT_TOKEN not configured"}
        
        if not target_chat:
            return False, {"error": "TELEGRAM_GROUP_ID not configured"}
        
        # Calculate expiry timestamp
        expire_date = int(datetime.now(timezone.utc).timestamp()) + expire_seconds
        
        params = {
            "chat_id": target_chat,
            "member_limit": 1,  # 🔐 KEY: Only 1 person can use this link!
            "expire_date": expire_date,
            "creates_join_request": False  # Direct join, no approval needed
        }
        
        if name:
            # Telegram allows max 32 chars for name
            params["name"] = name[:32]
        
        logger.info(f"🎟️ Creating one-time invite for chat {target_chat} (expires in {expire_seconds}s)")
        
        result = await self._api_request("createChatInviteLink", params)
        
        if result.get("ok"):
            invite_data = result.get("result", {})
            invite_link = invite_data.get("invite_link", "")
            
            logger.info(f"✅ One-time link created: {invite_link[:30]}...")
            
            return True, {
                "invite_link": invite_link,
                "name": invite_data.get("name"),
                "expire_date": invite_data.get("expire_date"),
                "member_limit": invite_data.get("member_limit"),
                "is_one_time": True
            }
        else:
            error = result.get("error", "Unknown error")
            logger.error(f"❌ Failed to create invite: {error}")
            return False, {"error": error}
    
    async def revoke_invite(self, invite_link: str, chat_id: Optional[str] = None) -> bool:
        """
        Widerruft einen Invite Link
        
        Args:
            invite_link: Der komplette Invite Link
            chat_id: Optional Chat ID
        
        Returns:
            True wenn erfolgreich
        """
        target_chat = chat_id or self.default_group_id
        
        result = await self._api_request("revokeChatInviteLink", {
            "chat_id": target_chat,
            "invite_link": invite_link
        })
        
        return result.get("ok", False)
    
    async def get_chat_info(self, chat_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Holt Informationen über die Gruppe
        
        Returns:
            Chat Info (title, type, member_count, etc.)
        """
        target_chat = chat_id or self.default_group_id
        
        if not target_chat:
            return {"ok": False, "error": "No chat ID"}
        
        result = await self._api_request("getChat", {"chat_id": target_chat})
        
        if result.get("ok"):
            chat = result.get("result", {})
            return {
                "ok": True,
                "title": chat.get("title"),
                "type": chat.get("type"),
                "id": chat.get("id"),
                "username": chat.get("username"),
                "invite_link": chat.get("invite_link")  # Permanent link (if set)
            }
        
        return result


# Singleton Instance
telegram_bot = TelegramBotService()


# ===== CONVENIENCE FUNCTIONS =====

async def create_one_time_telegram_invite(
    wallet_address: str,
    group_id: Optional[str] = None,
    expire_seconds: int = 300
) -> Tuple[bool, str]:
    """
    Convenience Function: Erstellt Einmal-Link für Wallet
    
    Args:
        wallet_address: Ethereum Wallet Adresse
        group_id: Optional eigene Group ID (sonst default)
        expire_seconds: Gültigkeit (default 5 Min)
    
    Returns:
        (success, invite_link_or_error)
    """
    # Create short name from wallet
    name = f"VEra-{wallet_address[:8]}"
    
    success, result = await telegram_bot.create_one_time_invite(
        chat_id=group_id,
        name=name,
        expire_seconds=expire_seconds
    )
    
    if success:
        return True, result.get("invite_link", "")
    else:
        return False, result.get("error", "Unknown error")


async def check_bot_setup() -> Dict[str, Any]:
    """
    Prüft ob Bot korrekt konfiguriert ist
    
    Returns:
        Status-Dict mit allen relevanten Infos
    """
    status = {
        "token_configured": bool(telegram_bot.bot_token),
        "group_configured": bool(telegram_bot.default_group_id),
        "bot_info": None,
        "permissions": None,
        "ready": False
    }
    
    if not status["token_configured"]:
        status["error"] = "TELEGRAM_BOT_TOKEN not set in .env"
        return status
    
    if not status["group_configured"]:
        status["error"] = "TELEGRAM_GROUP_ID not set in .env"
        return status
    
    # Check bot info
    bot_result = await telegram_bot.get_bot_info()
    if bot_result.get("ok"):
        status["bot_info"] = telegram_bot._bot_info
    else:
        status["error"] = f"Bot token invalid: {bot_result.get('error')}"
        return status
    
    # Check permissions
    perm_result = await telegram_bot.verify_bot_permissions()
    status["permissions"] = perm_result
    
    if perm_result.get("ok") and perm_result.get("can_invite"):
        status["ready"] = True
        status["message"] = f"✅ Bot @{status['bot_info'].get('username')} ready!"
    else:
        status["error"] = perm_result.get("error", "Bot lacks invite permissions")
    
    return status


# ===== GROUP BOT INTEGRATION =====

def store_capabilities_for_invite(invite_link: str, score: int, min_score: int = 50):
    """
    Speichert Capabilities für einen Invite-Link
    
    Wird vom Gate-Prozess aufgerufen BEVOR der Link an den User geht.
    Der Group Bot holt diese dann wenn der User beitritt.
    
    Args:
        invite_link: Der erstellte Telegram Invite Link
        score: Resonance Score des Users (wird in Capabilities umgewandelt)
        min_score: Mindest-Score für Schreibrechte
    """
    try:
        # Import hier um circular imports zu vermeiden
        from telegram_group_bot import group_bot
        
        # Generiere Capabilities basierend auf Score
        capabilities = []
        
        # Schreibrechte wenn Score >= min_score
        if score >= min_score:
            capabilities.append("write")
        
        # Poll-Capabilities für alle erreichbaren Stufen
        poll_levels = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        for level in poll_levels:
            if score >= level:
                capabilities.append(f"poll_{level}")
        
        # Bei Group Bot registrieren
        group_bot.session_manager.store_pending_token(
            invite_link=invite_link,
            capabilities=capabilities,
            expire_seconds=120  # 2 Minuten Zeit zum Beitreten
        )
        
        logger.info(f"✅ Capabilities stored for invite: {capabilities}")
        return True
        
    except ImportError:
        # Group Bot nicht verfügbar - kein Problem, läuft auch ohne
        logger.debug("Group Bot not available - skipping capability storage")
        return False
    except Exception as e:
        logger.warning(f"Could not store capabilities: {e}")
        return False


async def create_one_time_telegram_invite_with_capabilities(
    wallet_address: str,
    score: int,
    min_score: int = 50,
    expire_seconds: int = 300
) -> Tuple[bool, str]:
    """
    Erstellt Einmal-Link UND registriert Capabilities für Group Bot
    
    Kombiniert:
    1. create_one_time_telegram_invite() - Link erstellen
    2. store_capabilities_for_invite() - Capabilities für Group Bot
    
    Args:
        wallet_address: Für Link-Name (anonymisiert)
        score: Resonance Score
        min_score: Mindest-Score für Schreibrechte
        expire_seconds: Link-Gültigkeit
    
    Returns:
        (success, invite_link_or_error)
    """
    # 1. Link erstellen
    success, result = await create_one_time_telegram_invite(
        wallet_address=wallet_address,
        expire_seconds=expire_seconds
    )
    
    if not success:
        return False, result
    
    invite_link = result
    
    # 2. Capabilities für Group Bot speichern
    store_capabilities_for_invite(
        invite_link=invite_link,
        score=score,
        min_score=min_score
    )
    
    return True, invite_link


# ===== CLI TEST =====
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("🤖 Testing Telegram Bot Service...\n")
        
        # Check setup
        status = await check_bot_setup()
        print(f"Configuration Status:")
        print(f"  Token: {'✅' if status['token_configured'] else '❌'}")
        print(f"  Group: {'✅' if status['group_configured'] else '❌'}")
        
        if status.get("bot_info"):
            print(f"  Bot: @{status['bot_info'].get('username')}")
        
        if status.get("permissions"):
            print(f"  Permissions: {status['permissions'].get('message', status['permissions'])}")
        
        if status["ready"]:
            print(f"\n✅ {status['message']}")
            
            # Test creating a link
            print("\n📝 Creating test one-time invite...")
            success, link = await create_one_time_telegram_invite("0xTestWallet1234", expire_seconds=60)
            
            if success:
                print(f"✅ Link created: {link}")
                print("   ⚠️ This link will expire in 60 seconds and can only be used ONCE!")
            else:
                print(f"❌ Failed: {link}")
        else:
            print(f"\n❌ Not ready: {status.get('error')}")
    
    asyncio.run(test())
