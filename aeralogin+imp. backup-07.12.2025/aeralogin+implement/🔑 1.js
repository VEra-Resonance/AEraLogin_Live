🔑 1. Base unterstützt SIWE offiziell über WalletConnect-Like Capabilities
Base implementiert Sign-In With Ethereum (SIWE) als Capability im WalletConnect-Style, d.h. du kannst SIWE mit dem Base Wallet auslösen über:
provider.request({
  method: "wallet_connect",
  params: [{
    version: "1",
    capabilities: {
      signInWithEthereum: {
        nonce,
        chainId: "0x2105"  // Base Mainnet chain ID
      }
    }
  }]
});
Dabei gibt der Wallet-Provider ein Objekt mit:
message: die EIP-4361 SIWE Nachricht
signature: die Antwort-Signatur
zurück, die du serverseitig verifizieren kannst. 
Base-Dokumentation
🧠 2. SIWE für Base ist nach dem offenen Standard EIP-4361
Base folgt dem EIP-4361 SIWE-Standard, bei dem:
App erzeugt eine menschenlesbare SIWE-Nachricht (inkl. domain, nonce, chainId, ggf. uri)
Wallet der Nutzerin signiert diese Nachricht
Der Signature wird an deinen Server/Backend gesendet
Der Server verifiziert die Signatur → authentifiziert die Userin
Das ist nicht Coinbase-spezifisch, sondern SIWE nach Standard. 
docs.siwe.xyz
🔗 3. Wie Base Wallet SIWE im Frontend typischerweise genutzt wird
Je nachdem, welche Wallet-Lib du nutzt (z. B. OnchainKit, wagmi/viem):
📌 Mit OnchainKit/ConnectWallet
Du nutzt z. B.:
const message = createSiweMessage({
  address: userAddress,
  chainId: base.id,
  domain: window.location.host,
  nonce: nonce,
  uri: window.location.origin,
  version: "1",
});

signMessage({ message });
wobei signMessage die Base Wallet dazu bringt, genau diese SIWE-Message zu signieren. 
Base-Dokumentation
📡 4. Wichtige Details für Base-SIWE
✅ Nonce
Netter Zufallswert, der jede SIWE-Session einmalig macht.
Du musst ihn serverseitig erzeugen/verwalten, sonst können Signaturen erneut abgespielt werden. 
Base-Dokumentation
🔁 Chain ID
Base Mainnet hat Chain-ID 8453 → wird hexadezimal in der SIWE-Nachricht genutzt (0x2105). 
Base-Dokumentation
🖋 Signature
Die Wallet gibt dir die Signatur zur SIWE-Message zurück → diese muss serverseitig mit der SIWE-Bibliothek (z. B. siwe npm) validiert werden.
📌 5. Wichtige Implikation für die Implementierung
⚠️ Du musst SIWE über einen Wallet-Connector auslösen, der WalletCapability-SignInWithEthereum unterstützt –
bei Base geht das nur über WalletConnect-like Requests oder libs wie OnchainKit & wagmi + SignMessage.
→ Einfaches signMessage() reicht nicht immer, wenn keine Wallet-Capabilities gesetzt sind. 
Base-Dokumentation
📌 6. Server-Verifikation
Auf deinem Server verwendest du eine SIWE-Bibliothek (z. B. @siwe/siwe) um:
die eingehende SIWE-Message zu parsen
die Signatur zu validieren
Adresse, Domain, ChainID & Nonce zu prüfen
So erzeugst du eine echte authenticated Session.
🔎 Kurz gesagt
Wie die Base Wallet SIWE-Sign-in erwartet:
Du sendest eine signInWithEthereum-Capability-Request an den Wallet-Provider. 
Base-Dokumentation
Der Base Wallet antwortet mit SIWE-Message + Signatur. 
Base-Dokumentation
Du verifizierst die Signatur auf deinem Server nach dem EIP-4361-Standard. 
docs.siwe.xyz