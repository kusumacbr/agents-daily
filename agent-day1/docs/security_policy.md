# Acme Robotics - Information Security & IT Policy

**Document ID:** SEC-POL-002  
**Effective Date:** January 10, 2026  
**Owner:** Information Security & IT  
**Security Lead:** Neha Sharma (`security@acmerobotics.internal`)

---

## 1. Authentication & Passwords
- All company accounts (Google Workspace, GitHub Enterprise, AWS IAM) must enforce Multi-Factor Authentication (MFA) using hardware security keys (YubiKey) or TOTP authenticator apps. SMS-based 2FA is strictly prohibited.
- Passwords must be at least **14 characters long**, containing uppercase letters, lowercase letters, numbers, and symbols.
- Passwords must be changed every **90 days**.

## 2. Authorized Devices & Network Access
- Only company-provisioned machines running MDM (Jamf Pro for macOS, CrowdStrike Falcon on Linux/Windows) are permitted to connect to corporate networks.
- **Corporate Wi-Fi:** `Acme-Corp-Secure` uses 802.1X enterprise certificates installed during device provisioning.
- **Visitor Wi-Fi:** `Acme-Guest` is isolated from the internal LAN. Guest network access credentials are not published in internal documentation; visiting clients and guests must request a temporary one-day access voucher from the front desk reception.

## 3. Removable Media & Data Loss Prevention (DLP)
- Mass storage devices (USB thumb drives, external hard disks) are blocked by default by endpoint protection software.
- Exceptions for flashing robot firmware must be logged via IT ticket and approved by Neha Sharma.

## 4. Clean Desk & Screen Locking
- Screens must be locked automatically after **5 minutes of inactivity**.
- Physical keys, hardware prototypes, and access badges must not be left unattended at workstations overnight.
