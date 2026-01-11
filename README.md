# krishi_sajag
Krishi Sajag is an innovative, offline-first AI application designed to deliver timely and accurate agricultural advice to farmers in regions facing poor internet connectivity and significant language barriers.

# Problem Statement
Millions of farmers in India, particularly in rural and remote areas, suffer significant economic losses due to untimely and inaccurate diagnosis of crop diseases, pests, and nutrient deficiencies.

Digital Divide: Most advanced agricultural AI tools require constant, high-speed internet access, making them unusable in low-connectivity zones.
Literacy and Language Barriers: Information is often available only in English or complex technical jargon, preventing effective adoption by the local population.
Financial Impact: Delayed intervention—caused by waiting for experts or traveling long distances—leads directly to reduced yield and wasted resources (fertilizer, water).

# Proposed Solution
Krishi Sajag is an Offline AI Crop Advisor designed to deliver instant, hyper-localized, and multilingual advice directly to the farmer. The solution bypasses connectivity issues by moving the intelligence from the cloud to the device.

Core Principle: Offline-First. The entire knowledge base, built with Generative AI, resides locally.
Accessibility: Integrates multilingual support (Hindi, Telugu, English) and Speech-to-Text input for low-literacy users.
Usability: Provides clear, actionable, low-cost organic and scientific remedies, reducing the need for costly external expert consultation.

# How the Solution Works
Krishi Sajag operates on a simple, three-step, offline pipeline:

Input & Localization: The farmer accesses the app and selects their desired language (Hindi/Telugu/English). They enter symptoms either by typing or by clicking the "Use Voice Input" button.
Offline Query: The app immediately takes the user's input and queries the local SQLite database (knowledge.db). It uses keyword and symptom matching to identify the most likely disease or deficiency.
Localized Output: Once a match is found, the system retrieves the full set of structured advice (Symptoms, Cause, Remedies, Prevention) and displays it instantly in the farmer's selected mother tongue, using a clean, high-contrast interface.

# Use of APIs
Krishi Sajag strategically uses APIs during the setup phase to build its intelligence, minimizing reliance on APIs during the live, offline operation.
Used as the expert researcher and translator. The API was systematically prompted to generate accurate diagnostic information for hundreds of diseases and then reliably translate this content into structured Hindi and Telugu datasets.

# Impact
Krishi Sajag creates direct, measurable impact across four key areas:

Economic: Reduces crop loss by promoting timely intervention and lowers input costs by prioritizing low-cost, organic remedies.
Accessibility: Empowers farmers in non-English speaking, low-connectivity areas with expert knowledge previously unavailable to them.
Sustainability: Promotes the use of sustainable, organic treatments indexed by the Gemini AI, reducing reliance on expensive and harmful chemical fertilizers.
Empowerment: Increases the farmer's confidence and decision-making capacity, making them less dependent on external experts.

# Future Scope
The hybrid architecture of Krishi Sajag allows for powerful future extensions:

Offline Image Classification: Integrate a lightweight, pre-trained ML model (like MobileNetV2) converted to .tflite for fast, on-device image-based diagnosis.
Localized Resource Index: Integrate location data to recommend remedies that use locally available, specific materials (e.g., local neem variety, regional manure availability).
Predictive Risk Assessment: Use the localized SQLite database to integrate seasonal weather trends and advise farmers on which diseases they are most susceptible to before symptoms appear.
Scaling Content: Expand the knowledge base to cover regional crop varieties and localized pest infestations specific to each major Indian agro-climatic zone.
