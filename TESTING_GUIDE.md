# 🧪 KRISHI-DRISTI 2.0 - Testing Guide

## 📋 Table of Contents
- [Testing Overview](#testing-overview)
- [Manual Testing](#manual-testing)
- [Functional Testing](#functional-testing)
- [Cross-Browser Testing](#cross-browser-testing)
- [Mobile Device Testing](#mobile-device-testing)
- [Performance Testing](#performance-testing)
- [Accessibility Testing](#accessibility-testing)
- [Test Cases](#test-cases)
- [Bug Reporting](#bug-reporting)

---

## 🎯 Testing Overview

This guide provides comprehensive testing procedures for the KRISHI-DRISTI 2.0 crop price prediction system to ensure functionality, usability, and compatibility across all platforms and devices.

### Testing Objectives
- ✅ Verify all features work correctly
- ✅ Ensure responsive design on all devices
- ✅ Validate price prediction accuracy
- ✅ Test cross-browser compatibility
- ✅ Check accessibility standards
- ✅ Measure performance metrics

---

## 🔍 Manual Testing

### Test Environment Setup
1. **Desktop Browsers**: Chrome, Firefox, Safari, Edge
2. **Mobile Browsers**: iOS Safari, Chrome Mobile, Samsung Internet
3. **Devices**: Desktop, Laptop, Tablet, Smartphone
4. **Network**: WiFi, 4G/5G, Slow 3G (for performance testing)

### Pre-Testing Checklist
- [ ] All files are present (index.html, styles.css, script.js)
- [ ] CDN links are accessible (Chart.js, Google Fonts)
- [ ] No console errors on page load
- [ ] All images/icons load correctly
- [ ] Responsive design is enabled

---

## ⚙️ Functional Testing

### 1. Page Load Testing

#### Test Case: Initial Page Load
**Steps:**
1. Open the application URL
2. Observe page loading behavior

**Expected Results:**
- ✅ Page loads within 3 seconds
- ✅ Header displays "KRISHI" with wheat icon
- ✅ Gradient background renders correctly
- ✅ All form fields are visible
- ✅ No JavaScript errors in console

---

### 2. Form Validation Testing

#### Test Case 2.1: Crop Selection
**Steps:**
1. Click on "Select Crop" dropdown
2. Select "Wheat"
3. Observe state dropdown

**Expected Results:**
- ✅ Dropdown shows 8 crops
- ✅ State dropdown enables automatically
- ✅ State dropdown shows: Madhya Pradesh, Punjab, Uttar Pradesh

#### Test Case 2.2: State Selection
**Steps:**
1. Select different crops
2. Verify states update accordingly

**Expected Results for Each Crop:**
- **Wheat**: Madhya Pradesh, Punjab, Uttar Pradesh
- **Paddy**: Punjab, Uttar Pradesh, West Bengal
- **Cotton**: Gujarat, Maharashtra, Punjab
- **Maize**: Madhya Pradesh, Uttar Pradesh
- **Arhar**: Madhya Pradesh, Maharashtra, Uttar Pradesh
- **Moong**: Madhya Pradesh, Rajasthan
- **Mustard**: Madhya Pradesh, Rajasthan
- **Sugarcane**: Maharashtra, Uttar Pradesh

#### Test Case 2.3: Rainfall Input
**Steps:**
1. Click on rainfall input field
2. Enter various values: 0, 650.5, 1200, 5000
3. Test invalid inputs: -100, letters, symbols

**Expected Results:**
- ✅ Accepts decimal numbers (e.g., 650.5)
- ✅ Accepts range 0-5000
- ✅ Rejects negative numbers
- ✅ Rejects non-numeric input
- ✅ Placeholder shows examples

#### Test Case 2.4: Market Demand Input
**Steps:**
1. Enter demand values: 1000, 5000, 25000, 100000
2. Test edge cases: 0, 1000000

**Expected Results:**
- ✅ Accepts whole numbers
- ✅ Accepts range 0-1000000
- ✅ Shows quintal unit
- ✅ Placeholder displays examples

#### Test Case 2.5: Year and Month Selection
**Steps:**
1. Enter year: 2020, 2025, 2030
2. Select different months

**Expected Results:**
- ✅ Year accepts 2020-2030
- ✅ Default year is 2025
- ✅ All 12 months available
- ✅ Month names display correctly

#### Test Case 2.6: Required Field Validation
**Steps:**
1. Leave all fields empty
2. Click "Predict Price"

**Expected Result:**
- ✅ Browser shows validation message for first empty required field

---

### 3. Price Prediction Testing

#### Test Case 3.1: Basic Prediction
**Test Data:**
- Crop: Wheat
- State: Punjab
- Rainfall: 650mm
- Demand: 10000 quintals
- Year: 2025
- Month: March

**Steps:**
1. Fill all fields with test data
2. Click "Predict Price"
3. Wait for results

**Expected Results:**
- ✅ Results section appears smoothly
- ✅ Predicted price displays in ₹
- ✅ Confidence score shows (65-95%)
- ✅ Market insights populate
- ✅ Chart renders with data
- ✅ All result fields show correct input values

#### Test Case 3.2: Price Range Validation
**Test Multiple Scenarios:**

| Crop | Expected Range (₹/quintal) |
|------|---------------------------|
| Wheat | 1,500 - 2,500 |
| Paddy | 1,500 - 2,500 |
| Cotton | 4,500 - 7,500 |
| Maize | 1,400 - 2,400 |
| Arhar | 5,000 - 8,000 |
| Moong | 6,000 - 9,000 |
| Mustard | 4,500 - 6,500 |
| Sugarcane | 2,500 - 4,000 |

**Expected Result:**
- ✅ Predicted prices fall within reasonable ranges

#### Test Case 3.3: Demand Impact Testing
**Test Data (Same crop, different demand):**
1. Demand: 2000 quintals → Lower price expected
2. Demand: 50000 quintals → Higher price expected

**Expected Result:**
- ✅ Higher demand results in higher price
- ✅ Price difference is proportional

#### Test Case 3.4: Rainfall Impact Testing
**Test Scenarios:**
1. **Low Rainfall** (200mm) → Price increase (drought)
2. **Optimal Rainfall** (600mm for wheat) → Moderate price
3. **High Rainfall** (2000mm) → Price increase (crop damage)

**Expected Result:**
- ✅ Extreme rainfall increases price
- ✅ Optimal rainfall gives best (lowest) price

#### Test Case 3.5: Seasonal Impact
**Test Data (Same inputs, different months):**
1. Harvest month (March for wheat) → Lower price
2. Off-season month (September) → Higher price

**Expected Result:**
- ✅ Harvest season shows lower prices
- ✅ Off-season shows higher prices

---

### 4. Chart Visualization Testing

#### Test Case 4.1: Chart Display
**Steps:**
1. Complete a price prediction
2. Scroll to chart section

**Expected Results:**
- ✅ Chart renders without errors
- ✅ Shows "Actual Price" in blue
- ✅ Shows "Predicted Price" in red
- ✅ X-axis shows dates
- ✅ Y-axis shows prices in ₹
- ✅ Legend displays correctly
- ✅ Chart title shows crop name

#### Test Case 4.2: Chart Interactivity
**Steps:**
1. Hover over data points
2. Click on legend items

**Expected Results:**
- ✅ Tooltip shows exact price values
- ✅ Tooltip displays date
- ✅ Values formatted with ₹ symbol
- ✅ Smooth hover animations

#### Test Case 4.3: Multiple Predictions
**Steps:**
1. Make first prediction for Wheat
2. Make second prediction for Cotton
3. Observe chart update

**Expected Result:**
- ✅ Chart updates with new data
- ✅ Previous chart is replaced
- ✅ No duplicate charts appear

---

### 5. Reset Functionality Testing

#### Test Case 5.1: Form Reset
**Steps:**
1. Fill all form fields
2. Click "Reset" button

**Expected Results:**
- ✅ All fields clear to default
- ✅ State dropdown resets to "First select a crop..."
- ✅ State dropdown becomes disabled
- ✅ Results section hides
- ✅ Chart clears

---

## 🌐 Cross-Browser Testing

### Desktop Browsers

#### Chrome Testing
- [ ] All features work correctly
- [ ] CSS renders properly
- [ ] Chart.js loads and displays
- [ ] Animations smooth
- [ ] No console errors

#### Firefox Testing
- [ ] Form validation works
- [ ] Select dropdowns styled correctly
- [ ] Chart renders properly
- [ ] All interactions functional

#### Safari Testing
- [ ] iOS-specific styling correct
- [ ] Form inputs sized properly
- [ ] No webkit-specific issues
- [ ] Smooth scrolling works

#### Edge Testing
- [ ] Chromium-based features work
- [ ] Legacy Edge compatible (if needed)
- [ ] All styles render correctly

---

## 📱 Mobile Device Testing

### iOS Devices (Safari)

#### iPhone Testing (All Models)
**Test Devices:**
- iPhone SE (small screen)
- iPhone 13/14/15 (standard)
- iPhone 14/15 Pro Max (large screen)

**Test Cases:**
- [ ] Page fits screen without horizontal scroll
- [ ] Form inputs don't zoom on focus (16px minimum)
- [ ] Buttons are easily tappable (50px minimum)
- [ ] Chart is readable and interactive
- [ ] Portrait mode displays correctly
- [ ] Landscape mode layouts properly
- [ ] No webkit-specific bugs

#### iPad Testing
**Test Devices:**
- iPad Mini
- iPad Air
- iPad Pro

**Test Cases:**
- [ ] Two-column layout on tablets
- [ ] Touch targets appropriate size
- [ ] Chart uses available space
- [ ] Keyboard doesn't obscure inputs

### Android Devices

#### Samsung Testing
**Test Devices:**
- Galaxy S series (S21, S22, S23)
- Galaxy A series
- Galaxy Note series

**Test Cases:**
- [ ] Samsung Internet browser compatible
- [ ] Chrome mobile works perfectly
- [ ] Form inputs render correctly
- [ ] No Android-specific issues

#### Other Android Brands
- [ ] Oppo devices
- [ ] iQOO devices
- [ ] OnePlus devices
- [ ] Xiaomi devices
- [ ] Realme devices
- [ ] Vivo devices

### Responsive Breakpoints Testing

| Breakpoint | Screen Size | Layout |
|------------|-------------|--------|
| Small Mobile | < 480px | Single column, compact |
| Standard Mobile | 481-768px | Single column, standard |
| Tablet Portrait | 769-1024px | Two columns |
| Tablet Landscape | 1025-1280px | Two columns, wider |
| Desktop | > 1280px | Multi-column |

**Test Each Breakpoint:**
- [ ] Layout adapts correctly
- [ ] No content overflow
- [ ] Images scale properly
- [ ] Text remains readable
- [ ] Charts resize appropriately

---

## ⚡ Performance Testing

### Page Load Performance

#### Metrics to Measure:
- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3.0s
- **Total Blocking Time (TBT)**: < 200ms

#### Tools:
- Chrome DevTools (Lighthouse)
- PageSpeed Insights
- GTmetrix

### Network Performance

**Test Different Connections:**
- [ ] Fast 3G: Page loads in < 5s
- [ ] Slow 3G: Page loads in < 10s
- [ ] Offline: Shows appropriate error

### Resource Loading

**Check:**
- [ ] Chart.js CDN loads quickly
- [ ] Google Fonts load efficiently
- [ ] No blocking resources
- [ ] CSS/JS minified (if applicable)

---

## ♿ Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all form fields
- [ ] Enter submits form
- [ ] Esc clears/resets (if implemented)
- [ ] All interactive elements focusable

### Screen Reader Testing
- [ ] All labels read correctly
- [ ] Form fields have proper ARIA labels
- [ ] Error messages announced
- [ ] Results read in logical order

### Color Contrast
- [ ] Text meets WCAG AA standards (4.5:1)
- [ ] Buttons have sufficient contrast
- [ ] Links are distinguishable
- [ ] Chart colors are distinct

### Tools:
- WAVE Browser Extension
- axe DevTools
- Lighthouse Accessibility Audit

---

## 📝 Test Cases Summary

### Critical Test Cases (Must Pass)

| ID | Test Case | Priority | Status |
|----|-----------|----------|--------|
| TC-001 | Page loads successfully | High | ⬜ |
| TC-002 | Crop selection works | High | ⬜ |
| TC-003 | State updates based on crop | High | ⬜ |
| TC-004 | Price prediction calculates | High | ⬜ |
| TC-005 | Chart displays correctly | High | ⬜ |
| TC-006 | Mobile responsive design | High | ⬜ |
| TC-007 | Form validation works | High | ⬜ |
| TC-008 | Reset clears all fields | Medium | ⬜ |
| TC-009 | Results display correctly | High | ⬜ |
| TC-010 | Cross-browser compatible | High | ⬜ |

---

## 🐛 Bug Reporting

### Bug Report Template

```markdown
**Bug Title**: [Short description]

**Priority**: Critical / High / Medium / Low

**Environment**:
- Browser: 
- OS: 
- Device: 
- Screen Size: 

**Steps to Reproduce**:
1. 
2. 
3. 

**Expected Result**:
[What should happen]

**Actual Result**:
[What actually happened]

**Screenshots**:
[If applicable]

**Console Errors**:
[Any JavaScript errors]
```

### Where to Report
- GitHub Issues: https://github.com/anubhavy-05/KRISHI-DRISTI-2.0/issues

---

## ✅ Testing Checklist

### Pre-Release Testing
- [ ] All functional tests passed
- [ ] Cross-browser testing complete
- [ ] Mobile device testing complete
- [ ] Performance metrics acceptable
- [ ] Accessibility standards met
- [ ] No critical bugs remaining
- [ ] Documentation updated
- [ ] Code reviewed

---

## 📊 Test Results Log

### Testing Session Template

```
Date: [YYYY-MM-DD]
Tester: [Name]
Environment: [Browser/Device/OS]

Tests Performed:
- [ ] Functional Testing
- [ ] UI/UX Testing
- [ ] Performance Testing
- [ ] Accessibility Testing

Pass Rate: [X/Y tests passed]

Issues Found: [Number]
Critical: [Number]
High: [Number]
Medium: [Number]
Low: [Number]

Notes:
[Additional observations]
```

---

**Last Updated**: November 16, 2025  
**Version**: 2.0  
**Maintained By**: @anubhavy-05
