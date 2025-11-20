# Bug Reports

## Issue 1: Excessive Whitespace Between Form Checkboxes

**Summary:**
There is a large, unneeded vertical gap between the "I agree with your Privacy Policy" checkbox and the "This is a private computer, remember me" checkbox in the Contact/Help modal. This wastes screen real estate and pushes content further down unnecessarily.

**Steps to reproduce:**
1. Navigate to `https://www.optibet.lv/`.
2. Click on the "?" at the top right corner
3. Click on "reach us via contact form" and "let's have a chat"

**Actual Result:**
A significant vertical space exists between the two checkboxes.

**Expected Result:**
The checkboxes should be grouped closer together with standard vertical spacing (e.g., 8px-16px) to keep the form compact.

**Severity:** Low (Cosmetic)
**Priority:** Low


<img width="406" height="440" alt="image" src="https://github.com/user-attachments/assets/4f40857b-9fe2-4046-b21f-24e9b81404e9" />


---

## Issue 2: Unnecessary Vertical Scrollbar on Contact Form

**Summary:**
A vertical scrollbar is displayed on the right side of the Contact/Help modal even though there appears to be plenty of space to display the entire form without scrolling, or the content could be fit within the viewport without it. This clutters the UI.

**Steps to reproduce:**
1. Navigate to `https://www.optibet.lv/`.
2. Click on the "?" at the top right corner
3. Click on "reach us via contact form"
**Actual Result:**
A gray vertical scrollbar track is visible.

**Expected Result:**
The modal should auto-expand to fit its content without a scrollbar, or the scrollbar should only appear if the viewport height is actually smaller than the form content.

**Severity:** Low (Cosmetic/UX)
**Priority:** Low

<img width="407" height="440" alt="image" src="https://github.com/user-attachments/assets/fdab312c-86ee-424b-92d4-9c09747d0379" />


---

## Issue 3: Visual Artifact (Three Dots) at Bottom Right of Modal

**Summary:**
There are three small dots (`...`) visible at the very bottom right corner of the Contact/Help modal, just below the scrollbar track. This looks like a UI artifact, possibly from an overflow indicator or a misaligned element, and does not appear to serve a functional purpose.

**Steps to reproduce:**
1. Navigate to `https://www.optibet.lv/`.
2. Click on the "?" at the top right corner
3. Click on "reach us via contact form" and "let's have a chat"

**Actual Result:**
Three small dots are visible in the corner.

**Expected Result:**
The modal border/corner should be clean without unexplained visual artifacts.

**Severity:** Low (Cosmetic)
**Priority:** Low

<img width="407" height="440" alt="image" src="https://github.com/user-attachments/assets/189a1534-cd10-4b52-b553-1379b281cb1b" />




