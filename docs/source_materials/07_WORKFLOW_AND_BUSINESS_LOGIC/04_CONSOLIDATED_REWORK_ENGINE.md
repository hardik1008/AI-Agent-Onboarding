# Consolidated Rework Engine & Bi-Lingual Communication Specification

> **Engineering Specification for Single-Pass Rework Aggregation & Automated Messaging**  
> **Source:** Rulebook v3.2 §8 & Baseline Defect Pareto Analysis

---

## 1. The Single-Pass Principle

In historical operations, reviewers frequently issued fragmented rework queries (e.g., asking for a new marksheet on Monday, and then asking for a new bank cheque on Wednesday). This created severe applicant frustration, pushed average touches to 3.0, and drove a 33.2% dropout rate.

**The Single-Pass Rule:**
The system must inspect all 5 uploaded documents completely before dispatching any rework request. All defects across the entire application must be consolidated into a **single comprehensive message** containing targeted instructions and deep-links for each defective item.

---

## 2. Notification Message Templates (English & Hindi)

### 2.1 Image Quality Defects (`IMAGE_BLURRY`, `IMAGE_CROPPED`, `IMAGE_GLARE`)
- **English:**
  > *"Dear {applicant_name}, your {document_name} photo could not be verified because {specific_defect_reason}. Please take a new clear photo in bright daylight ensuring all four corners are visible, and upload it here: {secure_reupload_link}"*
- **Hindi:**
  > *"प्रिय {applicant_name}, आपके {document_name} की फ़ोटो सत्यापित नहीं हो सकी क्योंकि {hindi_defect_reason}। कृपया दिन की अच्छी रोशनी में चारों कोनों को दिखाते हुए एक नई साफ़ फ़ोटो लें और यहाँ अपलोड करें: {secure_reupload_link}"*

### 2.2 Name Spelling Variant (`NAME_SPELLING_VARIANT`)
- **English:**
  > *"Dear {applicant_name}, the name on your {document_name} ({extracted_name}) differs slightly from your PAN card ({pan_name}). If this is your document, please confirm your correct legal name or upload supporting proof here: {secure_reupload_link}"*
- **Hindi:**
  > *"प्रिय {applicant_name}, आपके {document_name} पर दर्ज नाम ({extracted_name}) आपके पैन कार्ड के नाम ({pan_name}) से थोड़ा भिन्न है। कृपया अपने सही नाम की पुष्टि करें या सहायक प्रमाण यहाँ अपलोड करें: {secure_reupload_link}"*

### 2.3 Date of Birth Conflict (`DOB_MISMATCH`)
- **English:**
  > *"Dear {applicant_name}, the date of birth on your {document_name} ({doc_dob}) does not match your PAN card ({pan_dob}). Please upload a clear official birth proof or corrected document here: {secure_reupload_link}"*
- **Hindi:**
  > *"प्रिय {applicant_name}, आपके {document_name} पर जन्म तिथि ({doc_dob}) आपके पैन कार्ड ({pan_dob}) से मेल नहीं खाती है। कृपया सही जन्म प्रमाण पत्र यहाँ अपलोड करें: {secure_reupload_link}"*

### 2.4 Bank Account Name Conflict (`BANK_NAME_MISMATCH`)
- **English:**
  > *"Dear {applicant_name}, our banking verification returned the account holder name '{penny_drop_name}', which does not match your name. POSP commission can only be paid to your own individual account. Please upload a cancelled cheque or bank statement in your own name: {secure_reupload_link}"*
- **Hindi:**
  > *"प्रिय {applicant_name}, बैंक सत्यापन में खातेदार का नाम '{penny_drop_name}' प्राप्त हुआ है, जो आपके नाम से मेल नहीं खाता। कमीशन का भुगतान केवल आपके स्वयं के व्यक्तिगत खाते में किया जा सकता है। कृपया अपने नाम का चेक या बैंक विवरण यहाँ अपलोड करें: {secure_reupload_link}"*

### 2.5 Low Biometric Face Match (`FACE_MATCH_LOW`)
- **English:**
  > *"Dear {applicant_name}, your selfie could not be matched with the photograph on your PAN card. Please take a new live selfie in a well-lit room looking directly at the camera without wearing sunglasses, caps, or masks: {secure_reupload_link}"*
- **Hindi:**
  > *"प्रिय {applicant_name}, आपकी सेल्फ़ी आपके पैन कार्ड की फ़ोटो से मेल नहीं खा सकी। कृपया अच्छी रोशनी में कैमरे की ओर सीधे देखते हुए बिना चश्मे या टोपी के एक नई सेल्फ़ी यहाँ लें: {secure_reupload_link}"*

---

## 3. Targeted Deep-Link Architecture

When an applicant opens the secure re-upload link:
1. The applicant is authenticated via a time-limited cryptographically signed session token (HMAC-SHA256, 72-hour validity).
2. The user interface displays **ONLY** the defective documents requiring correction.
3. Previously approved documents are rendered with a green `VERIFIED` lock icon and cannot be modified or re-uploaded, preventing re-triggering of completed reviews.
