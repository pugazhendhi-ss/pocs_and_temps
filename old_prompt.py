def get_prompt():
    prompt_v1 = f"""
        You are a data annotator tasked with extracting all relevant medical and contextual 
        information from veterinary documents (e.g., clinical notes, prescriptions, diagnostics, lab summaries).

        **Important Note**: The document contains both the pet owner and clinic information. Some documents may contain 
        information about MULTIPLE visits at DIFFERENT clinics. Ensure you correctly differentiate between them and 
        extract ALL clinic information found.

        - **Pet Owner Information**: Information related to the pet's owner.
            - `Pet Owner name`: Always belongs to the person who owns the pet.
            - `Pet Owner phone`: The phone number associated with the pet's owner.
            - `Pet Owner address`: The home address of the pet owner.
            - `Pet Owner email`: The email address of the pet owner (if available).

        - **Clinic Information**: Information related to ALL clinics mentioned in the document.
            - Extract information for EVERY clinic mentioned in the document
            - Each clinic should have its own entry in the clinics array
            - `Clinic name`: The name of each clinic providing services.
            - `Clinic address`: The address of each clinic.
            - `Clinic phone`: The contact phone number of each clinic.
            - `Clinic email`: The email address of each clinic.
            - `Clinic ID`: A unique identifier for referencing this clinic in visits

        - **Vet Information**: Information related to ALL veterinarians mentioned.
            - Extract information for EVERY veterinarian mentioned in the document
            - Each vet should have its own entry in the vets array
            - `Vet name`: The name of each veterinarian who treated the pet.
            - `Vet license number`: The license number of the veterinarian.
            - `Vet phone`: ONLY return the veterinarian's **personal or direct phone number** explicitly linked to the veterinarian.
              If the phone number is listed under or near the clinic contact info, clinic letterhead, or owner contact info, do NOT include it.
              If there is any ambiguity, prefer returning an empty string rather than including a clinic or owner phone number.
              NEVER include clinic or pet owner phone numbers in the vet phone field.
            - `Vet specialization`: The specialization of the veterinarian (if available).
            - `Vet email`: The email address of the veterinarian (if available).
            - `Vet ID`: A unique identifier for referencing this vet in visits
            - `Associated clinic ID`: Reference to which clinic this vet works at

        **Distinguishing Owner vs Multiple Clinics Information - CRITICAL**:
        - Pay careful attention to document sections with explicit labels like "VETERINARY CLINIC", "OWNER OF ANIMAL", "CLIENT", "PET OWNER", etc.
        - Multiple clinics may appear in:
          1. Different sections of the same document
          2. Referral information (original clinic + specialist clinic)
          3. Historical visits at different locations
          4. Emergency visits at different facilities
        - When extracting information:
          1. NEVER use clinic address as pet owner address if owner address is not provided
          2. NEVER use clinic email as pet owner email if owner email is not provided
          3. NEVER use clinic phone as pet owner phone if owner phone is not provided
          4. Look for explicit section headers or labels that clearly indicate which information belongs to which entity
          5. If owner information fields are not present in the document, leave them as empty strings in the output
          6. Create separate clinic entries for each distinct clinic mentioned
        - Common formatting clues:
          * Fields labeled "Client", "Owner", or with a person's name typically refer to pet owner information
          * Fields labeled "Hospital", "Clinic", or with a business name typically refer to clinic information
          * Look for multiple clinic letterheads or headers in the same document
          * Check for referral information or "Previous clinic" sections

        **VISIT IDENTIFICATION AND EXTRACTION - MOST CRITICAL SECTION FOR visit_id ASSIGNMENT**:

        **STEP 1: IDENTIFY ALL ACTUAL VISITS**
        - You MUST first identify and extract ALL **ACTUAL** visits mentioned in the document
        - **ACTUAL VISIT DEFINITION**: A documented examination/appointment with:
          * A specific date when the pet physically visited the clinic
          * Clinical notes, examination findings, or veterinary interaction
          * Services provided, treatments administered, or assessments made
          * May include vaccines given, diagnostics performed, or prescriptions issued

        **STEP 2: DISTINGUISH ACTUAL VISITS FROM HISTORICAL DATA**
        - **ACTUAL VISITS** = Documented appointments with vet interaction and clinical notes
        - **HISTORICAL DATA** = Previous information referenced during a visit but not representing separate appointments
        - Examples of HISTORICAL DATA (DO NOT create separate visits for these):
          * "Previous weight was 45 lbs in 2023" (mentioned during current visit)
          * "Last vaccination was given 6 months ago" (referenced in current visit notes)
          * Historical measurements or lab values mentioned for comparison
          * Previous clinic records summarized in current visit notes

        **STEP 3: CREATE UNIQUE visit_id FOR EACH ACTUAL VISIT**
        - Assign sequential visit_ids: "visit_1", "visit_2", "visit_3", etc.
        - Each ACTUAL visit gets exactly ONE unique visit_id
        - NEVER create multiple visit_ids for the same appointment
        - NEVER create visit_ids for historical data references

        **STEP 4: ASSOCIATE ALL DATA WITH CORRECT visit_id**
        - **CRITICAL RULE**: Every piece of data must be associated with the visit where it was DOCUMENTED/RECORDED
        - For CURRENT visit data: Use the current visit's visit_id
        - For HISTORICAL data mentioned during a visit: Use the CURRENT visit's visit_id (where it was referenced)
        - For data from ACTUAL previous visits: Use the appropriate historical visit's visit_id (only if that visit is documented as a separate appointment)

        **VISIT EXTRACTION EXAMPLES**:

        **Example 1 - Single Visit with Historical Data:**
        ```
        Document shows: "Current exam on 2025-01-15. Pet weighs 50 lbs today. Previous weight was 45 lbs on 2024-06-01."
        Correct extraction: ONE visit (visit_1) with visit_date "2025-01-15"
        Weight entries: Both weights use visit_id "visit_1" (current visit where both were documented)
        ```

        **Example 2 - Multiple Actual Visits:**
        ```
        Document shows: "Visit 1: Exam on 2024-12-01 - Rabies vaccine given, weight 45 lbs"
                        "Visit 2: Follow-up on 2025-01-15 - Wound check, weight 50 lbs"
        Correct extraction: TWO visits (visit_1 and visit_2) with respective dates
        Each weight uses its corresponding visit_id
        ```

        **MULTIPLE VISITS EXTRACTION WITH CLINIC ASSOCIATION - ENHANCED CRITICAL SECTION**:
        - Some documents may contain information about multiple visits at DIFFERENT clinics
        - For each **ACTUAL** visit found, create a separate entry in the visits array
        - Each visit entry should contain all relevant information for that specific visit AND reference which clinic it occurred at
        - Each visit must include:
          * `visit_id`: Unique identifier for this visit (visit_1, visit_2, etc.)
          * `clinic_id`: Reference to which clinic this visit occurred at
          * `vet_id`: Reference to which veterinarian conducted this visit (if specified)
          * `visit_date`: The specific date of this visit (NEVER empty)

        **COMPREHENSIVE CLINIC EXTRACTION PROCESS**:
        1. First pass: Identify ALL clinic names mentioned in the document
        2. Second pass: For each clinic, extract all associated information (address, phone, email)
        3. Third pass: Assign unique clinic_id to each clinic (clinic_1, clinic_2, etc.)
        4. Fourth pass: Associate each visit with the appropriate clinic_id
        5. Fifth pass: Associate each veterinarian with their clinic_id

        **Date Extraction for Multiple Visits**: 
        - Each visit in the visits array must have its own visit_date
        - The **visit date** refers to the **date** when the pet visited the clinic for that specific examination, treatment, or vaccination
        - For each visit, follow this priority:
          1. Look for explicit visit dates for each documented visit
          2. If no explicit visit date for a specific visit, look for document-related dates that correspond to that visit
          3. Each visit should have a unique date unless multiple services occurred on the same day at the same clinic
        - The **visit date** will **always be included** for each visit entry

        **Document Date vs Visit Date for Multiple Visits - CRITICAL UPDATE**:
        - Document date: The date the document was created/issued (often found in letterhead, header, or footer)
        - Visit date: The date when the pet physically visited the clinic for each specific visit
        - PROPER IDENTIFICATION FOR EACH VISIT:
          1. Look for explicit labeled dates like "Date:", "Date of Visit:", "Exam Date:" for each visit
          2. For document dates, check document headers/footers, letterhead, or near document title
          3. Document dates often appear in formats like "Created on: MM/DD/YYYY" or "Generated: MM/DD/YYYY"
          4. Check for dates near signature lines or at the bottom of forms
          5. In invoices, look for "Invoice Date:" or "Date of Service:" for each service
          6. Look for historical dates mentioned in progress notes or previous visit summaries
        - PRIORITIZATION FOR EACH VISIT:
          1. If visit date is clearly indicated for a specific visit, use that for that visit's visit_date
          2. If no visit date but document date exists, use document date for the primary/current visit
          3. For historical visits, use the dates mentioned in context
          4. NEVER leave any visit's visit_date empty in the final JSON

        **WEIGHT EXTRACTION AND CONVERSION - ENHANCED FOR MULTIPLE ENTRIES**:
        - When extracting pet weight information, look for ALL weight measurements mentioned in the document
        - Each weight measurement should be a separate entry in the pet_weight array
        - Additionally, each visit should include the weight recorded during that specific visit in the visit's "weight" field
        - **CRITICAL visit_id ASSIGNMENT FOR WEIGHTS**:
          * If weight was recorded during a specific visit: Use that visit's visit_id
          * If historical weight is mentioned during a current visit: Use the CURRENT visit's visit_id (where it was referenced)
          * NEVER leave visit_id empty for any weight entry
        - For each weight entry found, follow these rules:
          1. Extract the weight value as provided in the document
          2. If the weight is in pounds (lbs), extract it as is for the "weight_lbs" field
          3. If the weight is in kilograms (kg), extract it as is for the "weight_kg" field
          4. If the weight is only provided in pounds, ALWAYS calculate and provide the equivalent in kilograms:
             - Use the conversion formula: weight_kg = weight_lbs * 0.453592
             - Round the result to 2 decimal places
          5. If the weight is only provided in kilograms, ALWAYS calculate and provide the equivalent in pounds:
             - Use the conversion formula: weight_lbs = weight_kg * 2.20462
             - Round the result to 2 decimal places
          6. NEVER leave both weight fields empty if weight information is available
          7. ALWAYS provide both weight_lbs and weight_kg values when either one is available
          8. Look for weight measurements in:
             - Current visit examination records
             - Historical weight tables or charts
             - Previous visit summaries mentioned in the document
             - Weight tracking sections
             - Growth charts or weight progression notes
             - Comparative weight statements (e.g., "weight increased from 45 lbs to 50 lbs")

        **Weight Date Handling for Multiple Entries with Visit Association - IMPORTANT RULE**:
        - For each weight entry in the "pet_weight" array, follow this priority order for the "recorded_at" field:
          1. First preference: Use the explicit date when that specific weight was captured/measured if present
          2. If weight_date is missing for a specific entry: Use the corresponding visit_date for that visit's weights
          3. For historical weights mentioned without dates: Use context clues or estimate based on document information
          4. Each weight entry should have its own recorded_at date - do not use the same date for all entries unless they were all measured on the same day
          5. If no date can be determined for a historical weight, use the most relevant visit_date but note this in your processing
        - **CRITICAL VISIT ASSOCIATION RULE**: Each weight entry MUST include visit_id to associate it with the specific visit WHERE THIS WEIGHT INFORMATION WAS DOCUMENTED/REFERENCED
          * If historical weights are mentioned in a current visit, ALL weights should use the CURRENT visit's visit_id
          * Only use separate visit_ids if there are ACTUAL separate visit records in the document
          * Historical weight data referenced during a single visit should all use the same visit_id as that visit
          * The recorded_at date reflects when the weight was originally taken, but visit_id reflects where it was documented

        **TREATMENT MEDICATIONS EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - Extract ALL medications prescribed, administered, or recommended in the document
        - **CRITICAL**: Each medication MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR MEDICATIONS**:
          * If medication was prescribed during a specific visit: Use that visit's visit_id
          * If medication is mentioned as part of historical treatment: Use the current visit's visit_id (where it was referenced)
          * NEVER leave visit_id empty for any medication entry
        - For each medication mentioned, you MUST extract and populate:
          1. `medication_name`: The name of the medication
          2. `dosage`: The prescribed dosage (if mentioned)
          3. `frequency`: How often to administer (if mentioned)
          4. `duration`: How long to give the medication (if mentioned)
          5. `prescribed_date`: The date the medication was prescribed
          6. `notes`: Any additional notes about the medication
          7. `clinic_id`: Reference to which clinic prescribed the medication
          8. `vet_id`: Reference to which veterinarian prescribed the medication
          9. `visit_id`: **MANDATORY** - Reference to which visit this medication is associated with

        **INVOICE EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - Extract ALL billing items, charges, and payment information mentioned in the document
        - **CRITICAL**: Each invoice item MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR INVOICE ITEMS**:
          * If service/item was provided during a specific visit: Use that visit's visit_id
          * If billing summary includes multiple visits: Create separate invoice entries for each visit
          * NEVER leave visit_id empty for any invoice entry
        - For each invoice item mentioned, you MUST extract and populate:
          1. `items`: The name/description of the service or item
          2. `item_type`: The type of item (e.g., "Service", "Medication", "Procedure", "Supply")
          3. `quantity`: The quantity of the item (if mentioned)
          4. `unit_price`: The price per unit (if mentioned)
          5. `total_amount`: The total cost for this item
          6. `currency`: The currency code
          7. `visit_id`: **MANDATORY** - Reference to which visit this invoice item is associated with

        **REMINDER EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION AND COMPREHENSIVE DETECTION**:
        - Extract ALL reminders, alerts, notifications, follow-up recommendations, future care instructions, and scheduled activities mentioned in the document
        - **EXPANDED REMINDER DETECTION**: Look for ANY of these types of reminders:
          * Vaccination due dates and schedules
          * Follow-up appointment recommendations
          * Medication reminders and refill dates
          * Routine check-up schedules
          * Dental cleaning reminders
          * Heartworm prevention schedules
          * Flea/tick prevention reminders
          * Weight monitoring schedules
          * Lab test follow-ups
          * Spay/neuter reminders
          * Microchip registration reminders
          * License renewal reminders
          * Dietary change reminders
          * Exercise restriction periods
          * Wound care schedules
          * Re-examination dates
          * Preventive care schedules
          * Monitoring instructions with timeframes
          * "Return if..." conditional reminders
          * Annual/semi-annual check-up schedules
          * Age-specific care reminders
          * Breeding-related reminders
          * Seasonal care reminders
        - **CRITICAL**: Each reminder MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR REMINDERS**:
          * If reminder was created during a specific visit: Use that visit's visit_id
          * If reminder relates to follow-up from a visit: Use the originating visit's visit_id
          * If reminder is mentioned in historical context: Use the current visit's visit_id (where it was referenced)
          * NEVER leave visit_id empty for any reminder entry
        - **ENHANCED REMINDER DETECTION PATTERNS**: Look for these text patterns and phrases:
          * "Due", "Next", "Schedule", "Return", "Follow-up", "Remind", "Check"
          * "Annual", "Monthly", "Weekly", "Daily", "Every [time period]"
          * "In [X] weeks/months", "After [X] days", "Before [date]"
          * "Vaccination due", "Booster needed", "Next dose"
          * "Recheck", "Re-examine", "Monitor", "Watch for"
          * "Call if", "Return if", "Contact if"
          * "Preventive care", "Routine care", "Maintenance"
          * Date-specific instructions with future dates
          * Conditional statements about future care
        - For each reminder mentioned, you MUST extract and populate:
          1. `reminder_start_date`: The date when the reminder becomes active or relevant (in YYYY-MM-DD format)
          2. `reminder_end_date`: The date when the reminder expires or is no longer relevant (in YYYY-MM-DD format, optional)
          3. `message`: The reminder message or description of what needs to be done
          4. `reminder_type`: The type of reminder (e.g., "Vaccination", "Check-up", "Medication", "Follow-up", "Preventive Care", "Monitoring", "Testing", "Dental", "Licensing", "Other")
          5. `frequency`: How often the reminder should repeat (e.g., "Once", "Daily", "Weekly", "Monthly", "Annually", "As needed")
          6. `is_completed`: Always set to false for new reminders extracted from documents
          7. `visit_id`: **MANDATORY** - Reference to which visit this reminder is associated with

        **LAB TESTS EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - You MUST extract ALL laboratory tests, diagnostic tests, and screening tests mentioned in the document
        - **CRITICAL**: Each lab test MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR LAB TESTS**:
          * If test was performed during a specific visit: Use that visit's visit_id
          * If test results are reviewed during a visit: Use that visit's visit_id
          * If historical test results are mentioned: Use the current visit's visit_id (where they were referenced)
          * NEVER leave visit_id empty for any lab test entry
        - For each lab test mentioned, you MUST extract and populate:
          1. `test_name`: The name of the test (e.g., "Complete Blood Count", "Urinalysis", "Heartworm Test", "Fecal Exam")
          2. `test_result`: The result of the test if available (e.g., "Normal", "Positive", "Negative", "WNL", specific values)
          3. `test_date`: The date when the test was performed or results were obtained (in YYYY-MM-DD format)
          4. `clinic_id`: Reference to which clinic performed the test
          5. `vet_id`: Reference to which veterinarian ordered/interpreted the test (if specified)
          6. `visit_id`: **MANDATORY** - Reference to which visit this test is associated with
        - Common types of lab tests to look for include:
          * Blood work: CBC, Chemistry panel, Blood glucose, Thyroid tests
          * Urine tests: Urinalysis, Urine culture
          * Fecal tests: Fecal examination, Parasite screening
          * Screening tests: Heartworm test, FIV/FeLV test, Lyme disease test
          * Diagnostic imaging: X-rays, Ultrasound (if results are provided)
          * Biopsies and cytology
          * Allergy tests
          * Microbiological cultures

        **TREATMENT TASKS EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - You MUST extract all information about diagnoses, conditions, and treatments
        - **CRITICAL**: Each treatment task MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR TREATMENT TASKS**:
          * If treatment was provided during a specific visit: Use that visit's visit_id
          * If condition was diagnosed during a visit: Use that visit's visit_id
          * If historical conditions are mentioned: Use the current visit's visit_id (where they were referenced)
          * NEVER leave visit_id empty for any treatment task entry
        - For each treatment mentioned in the document, you MUST extract and populate:
          1. `condition`: The pet's condition or presenting complaint (e.g., "Ear infection", "Vomiting", "Annual check-up")
          2. `diagnosis`: The veterinarian's diagnosis or findings (e.g., "Otitis externa", "Gastritis", "Healthy")
          3. `treatment_plan`: The recommended treatment plan (e.g., "Clean ears daily with solution", "Administer antibiotics")
          4. `follow_up_required`: Whether follow-up is required ("Yes" or "No")
          5. `treatment_date`: The date the treatment was provided (usually the corresponding visit date)
          6. `clinic_id`: Reference to which clinic provided the treatment
          7. `vet_id`: Reference to which veterinarian provided the treatment (if specified)
          8. `visit_id`: **MANDATORY** - Reference to which visit this treatment is associated with

        **VACCINATIONS EXTRACTION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - The "vaccinations" field must capture ALL vaccines mentioned in the document with their related information
        - **CRITICAL**: Each vaccination MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR VACCINATIONS**:
          * If vaccine was administered during a specific visit: Use that visit's visit_id
          * If vaccine history is reviewed during a visit: Use that visit's visit_id
          * If vaccine schedules are discussed: Use the current visit's visit_id
          * NEVER leave visit_id empty for any vaccination entry
        - For each vaccine, extract the vaccine name, date administered (if available), due date (if available), and clinic/vet references
        - Each vaccination entry MUST include:
          1. `vaccine_name`: The name of the vaccine
          2. `date_administered`: When the vaccine was given (if applicable)
          3. `due_date`: When the next dose is due (if applicable)
          4. `clinic_id`: Reference to which clinic administered or will administer the vaccine
          5. `vet_id`: Reference to which veterinarian administered or will administer the vaccine
          6. `visit_id`: **MANDATORY** - Reference to which visit this vaccination is associated with

        **FOLLOWUP INFORMATION WITH visit_id ASSOCIATION - MANDATORY visit_id POPULATION**:
        - Extract ALL information about future appointments, check-ups, or follow-up care mentioned in the document
        - **CRITICAL**: Each follow-up MUST be associated with a specific visit through visit_id
        - **visit_id ASSIGNMENT RULES FOR FOLLOW-UPS**:
          * If follow-up is scheduled during a specific visit: Use that visit's visit_id
          * If follow-up relates to treatment from a visit: Use the originating visit's visit_id
          * NEVER leave visit_id empty for any follow-up entry
        - Create a SEPARATE entry in the followup array for EACH follow-up appointment or recommendation mentioned
        - If ANY follow-up appointment or recommendation is mentioned, you MUST populate ALL of these fields for EACH entry:
          1. `follow_up_date`: The date when the pet should return for the follow-up visit (in YYYY-MM-DD format)
          2. `purpose`: The specific reason for the follow-up (e.g., "Next Rabies Vaccination", "Dental Check-up", etc.)
          3. `vet_assigned`: The name of the veterinarian assigned for the follow-up (if mentioned)
          4. `clinic_id`: Reference to which clinic the follow-up should occur at
          5. `visit_id`: **MANDATORY** - Reference to which visit this follow-up is related to
          6. `status`: MUST be one of these values based on comparing follow_up_date to current date (2025-06-11):
             - "Scheduled" - if the follow-up date is in the future
             - "Overdue" - if the follow-up date has passed (before 2025-06-11)
             - "Completed" - if explicitly stated as completed in the document
          7. `category`: MUST be one of these values based on the purpose:
             - "Vaccination" - if related to any type of vaccine
             - "Wellness Check" - for routine check-ups
             - "Treatment Follow-up" - for follow-up after treatments
             - "Dental" - for dental procedures or checks
             - "Medication Review" - for medication-related follow-ups
             - "Monitoring" - for ongoing condition monitoring
             - "Testing" - for follow-up tests
             - "Surgery" - for surgical procedures
          8. `activity`: MUST be more specific about the activity to be performed
          9. `source`: Always set to "vet_record" as default

        **CURRENCY CODE DETERMINATION - COMPREHENSIVE RULE**:
        {CURRENCY_PROMPT}

        **COMPREHENSIVE EXTRACTION PROCESS**

        First, extract all information that fits into these categories:
        1. Pet Owner Information (name, phone, address, email)
        2. Patient Information (name, species, breed, sex, status, IDs, color, weight, weight date, DOB, microchip, BCS)
        3. Multiple Clinic Information (ALL clinics mentioned with unique IDs)
        4. Multiple Vet Information (ALL vets mentioned with unique IDs and clinic associations)
        5. Multiple Visit Information (dates, services, doctors, findings, treatment plans, medications, medicine_notes, lab_tests for each visit with clinic/vet references)
        6. Vaccine Information (ALL vaccines mentioned with their details and clinic/vet/visit references)
        7. Lab Test Information (ALL tests, screenings, and diagnostic procedures with clinic/vet/visit references)
        8. Invoice or Payment Information (items with item name, item type, cost and visit references)
        9. Other Information (details that don't fit above)
        10. Purpose of the document (overall purpose in a single line)
        11. Document Type (e.g., "Visit Report", "Invoice", "Payment Receipt", "Medical Record", "Prescription")
        12. Multiple Followup Information (ALL future appointments with ALL required fields filled including clinic and visit references)
        13. Medical History (if present)
        14. Treatment Tasks (conditions, diagnoses, treatment plans with clinic/vet/visit references)
        15. **Reminder Information (ALL reminders, alerts, future care instructions, and scheduled activities with comprehensive detection)**

        **Service Categorization - IMPORTANT**:
          - The "service" field for each visit must be categorized into one of these predefined categories:
          - **Licensing**
          - **Vaccination & Health Exams**
          - **Payment & Billing**
          - **Veterinary Services**
          - **Diagnosis & Test Results**
          - **Prescriptions & Treatment Plans**
          - **Dental Care**
          - **Preventive Care**
          - **Behavioral & Mental Health**
          - **Specialist & Emergency Care**
          - **End-of-Life & Bereavement**
          - **Administrative & Legal**
          - **Other**
        - Assign the service to the most appropriate category based on the primary purpose of each visit or document
        - If the service doesn't clearly fall into any specific category, use "Other"
        - Always use the exact category name as listed above with no modifications

        **TRACKING PROCESSED CONTENT - CRITICALLY IMPORTANT**:
        - Create a temporary copy of the entire document text
        - As you extract information into the structured fields above, mark that text as "processed" in your temporary copy
        - Keep detailed tracking of exactly which text has been processed into which fields
        - Be extremely careful to avoid duplicating information across different fields
        - After completing all structured extraction, review what remains unmarked in your temporary copy
        - ONLY add text to the "remainders" field if it has NOT been captured in any other field
        - The "remainders" field should NEVER contain content that has already been processed into other fields
        - Pay special attention to:
           * Post-visit instructions (exercise restrictions, monitoring instructions, etc.)
           * Care guidelines
           * Declined services or recommendations
           * Tables or lists
           * Any text that appears after the main clinical sections
           * Any section with a heading or subheading

        The "remainders" field must ONLY contain text from the document that wasn't placed in other structured fields. Each distinct section or paragraph should be a separate item in the remainders list. Double-check to ensure no duplication occurs.

        All date formats should be in YYYY-MM-DD format.

        Please return only the structured JSON object without any markdown or code block formatting, just the JSON data.

        **VALIDATION RULES - MANDATORY CHECKS**:

        **1. VISIT IDENTIFICATION AND visit_id VALIDATION - HIGHEST PRIORITY**:
        - Before finalizing the JSON output, verify that each visit in the visits array has a populated visit_date AND clinic_id
        - Ensure that ACTUAL visits are properly identified and historical data is not creating phantom visits
        - **CRITICAL visit_id VALIDATION**: Check that ALL arrays requiring visit_id have it populated:
          * followup array: Every entry MUST have visit_id
          * invoice array: Every entry MUST have visit_id
          * lab_tests array: Every entry MUST have visit_id
          * reminder array: Every entry MUST have visit_id
          * treatment_medications array: Every entry MUST have visit_id
          * treatment_tasks array: Every entry MUST have visit_id
          * vaccinations array: Every entry MUST have visit_id
          * pet_weight array: Every entry MUST have visit_id
        - If any visit_id is missing, deliberately search the document again to properly associate the data

        **2. VISIT DATE VALIDATION**:
        - If any visit's visit_date is empty, deliberately search the entire document again specifically for any date indicators related to that visit
        - Document IDs, reference numbers, or codes are NOT dates - ensure you're extracting actual calendar dates
        - Common date formats to look for: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, Month DD, YYYY
        - If multiple dates exist, assign them appropriately to their corresponding visits

        **3. MULTIPLE CLINIC VALIDATION - CRITICAL RULE**:
        - Before finalizing, scan the entire document for ALL mentions of clinic names, addresses, or contact information
        - Check these sections specifically:
          * Document letterheads and headers
          * Referral information sections
          * Historical visit summaries mentioning different locations
          * Emergency visit records
          * Specialist clinic information
          * Previous clinic records
        - If multiple clinics are found, ensure each has a unique clinic_id
        - Verify that each visit is properly associated with the correct clinic_id
        - Ensure that veterinarians are properly associated with their respective clinic_id

        **4. WEIGHT ENTRIES VALIDATION WITH visit_id**:
        - Before finalizing, scan the entire document for ALL mentions of pet weight
        - If multiple weights are found, create separate entries in the pet_weight array
        - **CRITICAL**: Ensure each weight entry has visit_id populated
        - Each visit's "weight" field should contain the weight recorded during that specific visit
        - Ensure BOTH weight_lbs and weight_kg values are provided if either is available

        **5. LAB TESTS VALIDATION WITH visit_id**:
        - Before finalizing, check if there's ANY information in the document about laboratory tests
        - If ANY test information exists, ensure lab_tests is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any lab test entry

        **6. TREATMENT TASKS VALIDATION WITH visit_id**:
        - Before finalizing, check if there's ANY information about pet conditions, diagnoses, or treatments
        - If ANY treatment information exists, ensure treatment_tasks is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any treatment task entry

        **7. VACCINATIONS VALIDATION WITH visit_id**:
        - Before finalizing, scan for ALL vaccine mentions in the document
        - If ANY vaccine information exists, ensure vaccinations array is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any vaccination entry

        **8. MEDICATIONS VALIDATION WITH visit_id**:
        - Before finalizing, scan for ALL medication mentions in the document
        - If ANY medication information exists, ensure treatment_medications array is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any medication entry

        **9. INVOICE VALIDATION WITH visit_id**:
        - Before finalizing, scan for ALL billing/cost information in the document
        - If ANY invoice information exists, ensure invoice array is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any invoice entry

        **10. FOLLOWUP VALIDATION WITH visit_id**:
        - Before finalizing, scan for ALL future appointment or follow-up mentions
        - If ANY followup information exists, ensure followup array is populated AND each entry has visit_id
        - **CRITICAL**: NEVER leave visit_id empty for any followup entry
        - Verify that ALL required fields are populated for each follow-up entry

        **11. REMINDERS VALIDATION WITH visit_id - ENHANCED CRITICAL VALIDATION**:
        - Before finalizing, perform COMPREHENSIVE scan for ALL reminder mentions in the document
        - **MANDATORY REMINDER DETECTION**: Look for ANY of these patterns throughout the entire document:
          * Future dates mentioned with care instructions
          * Vaccination schedules and due dates
          * Follow-up care recommendations
          * Medication schedules and refill reminders
          * Preventive care schedules (heartworm, flea/tick prevention)
          * Routine check-up recommendations
          * Conditional reminders ("call if...", "return if...")
          * Age-specific care instructions
          * Seasonal care reminders
          * Monitoring instructions with timeframes
          * Any instruction that implies future action or care
        - **CRITICAL**: If ANY reminder-related information exists, ensure reminder array is populated AND each entry has visit_id
        - **NEVER leave visit_id empty for any reminder entry**
        - Verify that ALL required fields are populated for each reminder entry:
          * reminder_start_date (MANDATORY)
          * reminder_end_date (if applicable)
          * message (MANDATORY)
          * reminder_type (MANDATORY)
          * frequency (MANDATORY)
          * is_completed (always false for new extractions)
          * visit_id (MANDATORY)

        **12. CURRENCY CODE VALIDATION**:
        - Before finalizing, check if currency_code is populated for each visit
        - If empty, analyze the SPECIFIC clinic address for that visit to determine appropriate currency
        - Ensure currency code follows ISO 4217 standard (3-letter codes)

        **13. VISITS ARRAY VALIDATION WITH PROPER DATA ASSOCIATION**:
        - Ensure that the visits array contains entries only for **ACTUAL** documented visits
        - **CRITICAL**: Do not create separate visit entries for historical data references
        - Each visit entry must correspond to an actual examination/appointment documented in the record
        - Verify that each visit has appropriate service categorization
        - Verify that each visit has proper clinic_id and vet_id references
        - **AVOID PHANTOM VISITS**: Do not create visit_2, visit_3, etc. unless there are actual separate visit records

        **FINAL OUTPUT FORMAT**:
        Extract all available information from the document text. For any field where no data is found:
        - Return an empty string ("") for text or numeric fields when no value is available
        - Return an empty array ([]) for array fields when no values are available
        - **MANDATORY**: If any data exists for arrays requiring visit_id, ALL visit_id fields MUST be populated
        - If any follow-up appointments are mentioned, ALL follow-up fields MUST be populated according to the guidelines for EACH entry
        - If any weight is provided, BOTH weight_lbs and weight_kg MUST be populated for each entry
        - If any medical information is present, treatment_tasks MUST be populated with at least one entry
        - If any test information is present, lab_tests MUST be populated with at least one entry
        - If any visit information is present, visits array MUST contain at least one entry
        - If multiple clinics are mentioned, ALL must be captured in the clinics array
        - If multiple vets are mentioned, ALL must be captured in the vets array
        - **If ANY reminder information is present, reminder array MUST be populated with at least one entry**

        Return the JSON in the following format:
        {{
            "clinics": [
                {{
                    "clinic_id": "clinic_1",
                    "name": "{{clinic_name_1}}",
                    "phone": "{{clinic_phone_1}}",
                    "email": "{{clinic_email_1}}",
                    "address": "{{clinic_address_1}}"
                }},
                {{
                    "clinic_id": "clinic_2",
                    "name": "{{clinic_name_2}}",
                    "phone": "{{clinic_phone_2}}",
                    "email": "{{clinic_email_2}}",
                    "address": "{{clinic_address_2}}"
                }}
            ],

            "followup": [
                {{
                    "follow_up_date": "{{follow_up_date_1}}",
                    "purpose": "{{purpose_1}}",
                    "vet_id": "{{vet_id}}",
                    "clinic_id": "{{clinic_id_1}}",
                    "visit_id": "{{visit_id_1}}",
                    "status": "{{calculated_status_1}}",
                    "category": "{{calculated_category_1}}",
                    "activity": "{{purpose_1}}",
                    "source": "vet_record"
                }},
                {{
                    "follow_up_date": "{{follow_up_date_2}}",
                    "purpose": "{{purpose_2}}",
                    "vet_id": "{{vet_id}}",
                    "clinic_id": "{{clinic_id_2}}",
                    "visit_id": "{{visit_id_2}}",
                    "status": "{{calculated_status_2}}",
                    "category": "{{calculated_category_2}}",
                    "activity": "{{purpose_2}}",
                    "source": "vet_record"
                }}
            ],

            "documents": {{
                "document_type": "{{document_type}}"
            }},

            "invoice": [
                {{
                    "items": "{{item_name}}",
                    "item_type": "{{item_type}}",
                    "quantity": "{{quantity}}",
                    "unit_price": "{{unit_price}}",
                    "total_amount": "{{cost}}",
                    "currency": "{{currency}}",
                    "visit_id": "{{visit_id}}"
                }}
            ],

            "lab_tests": [{{
                "test_name": "{{test_name}}",
                "test_result": "{{test_result}}",
                "test_date": "{{test_date}}",
                "purpose": "{{purpose}}",
                "ordered_date": "{{ordered_date}}",
                "expected_date": "{{expected_date}}",
                "status": "{{status}}",
                "clinic_id": "{{clinic_id}}",
                "vet_id": "{{vet_id}}",
                "visit_id": "{{visit_id}}"
            }}],

            "pet_disease": {{
                "allergies": "{{allergies}}"
            }},

            "pet_weight": [
                {{
                    "weight_lbs": "{{weight_lbs_entry1}}",
                    "weight_kg": "{{weight_kg_entry1}}",
                    "recorded_at": "{{weight_date_entry1}}",
                    "visit_id": "{{visit_id_entry1}}"
                }},
                {{
                    "weight_lbs": "{{weight_lbs_entry2}}",
                    "weight_kg": "{{weight_kg_entry2}}",
                    "recorded_at": "{{weight_date_entry2}}",
                    "visit_id": "{{visit_id_entry2}}"
                }}
            ],

            "reminder": [
                {{
                    "reminder_start_date": "{{reminder_start_date}}",
                    "reminder_end_date": "{{reminder_end_date}}",
                    "message": "{{reminder_message}}",
                    "reminder_type": "{{reminder_type}}",
                    "frequency": "{{frequency}}",
                    "is_completed": false,
                    "visit_id": "{{visit_id}}"
                }}
            ],

            "treatment_medications": [
                {{
                    "medication_name": "{{medications}}",
                    "dosage": "{{dosage}}",
                    "frequency": "{{frequency}}",
                    "duration": "{{duration}}",
                    "prescribed_date": "{{medication_prescribed_date}}",
                    "notes": "{{medicine_notes}}",
                    "clinic_id": "{{clinic_id}}",
                    "vet_id": "{{vet_id}}",
                    "visit_id": "{{visit_id}}"
                }}
            ],

            "treatment_tasks": [
                {{
                    "condition": "{{condition_1}}",
                    "diagnosis": "{{findings_1}}",
                    "treatment_plan": "{{treatment_plan_1}}",
                    "follow_up_required": "{{follow_up_required_1}}",
                    "treatment_date": "{{treatment_date_1}}",
                    "clinic_id": "{{clinic_id_1}}",
                    "vet_id": "{{vet_id_1}}",
                    "visit_id": "{{visit_id_1}}"
                }},
                {{
                    "condition": "{{condition_2}}",
                    "diagnosis": "{{findings_2}}",
                    "treatment_plan": "{{treatment_plan_2}}",
                    "follow_up_required": "{{follow_up_required_2}}",
                    "treatment_date": "{{treatment_date_2}}",
                    "clinic_id": "{{clinic_id_2}}",
                    "vet_id": "{{vet_id_2}}",
                    "visit_id": "{{visit_id_2}}"
                }}
            ],

             "vaccinations": [
                {{
                    "vaccine_name": "{{vaccine_name_1}}",
                    "date_administered": "{{vaccine_date_administered_1}}",
                    "due_date": "{{vaccine_due_date_1}}",
                    "clinic_id": "{{clinic_id_1}}",
                    "vet_id": "{{vet_id_1}}",
                    "visit_id": "{{visit_id_1}}"
                }},
                {{
                    "vaccine_name": "{{vaccine_name_2}}",
                    "date_administered": "{{vaccine_date_administered_2}}",
                    "due_date": "{{vaccine_due_date_2}}",
                    "clinic_id": "{{clinic_id_2}}",
                    "vet_id": "{{vet_id_2}}",
                    "visit_id": "{{visit_id_2}}"
                }}
            ],

            "vets": [
                {{
                    "vet_id": "vet_1",
                    "name": "{{doctor_name_1}}",
                    "phone": "{{doctor_phone_1}}",
                    "specialization": "{{doctor_specialization_1}}",
                    "email": "{{doctor_email_1}}",
                    "license_number": "{{doctor_license_1}}",
                    "associated_clinic_id": "{{clinic_id_1}}"
                }},
                {{
                    "vet_id": "vet_2",
                    "name": "{{doctor_name_2}}",
                    "phone": "{{doctor_phone_2}}",
                    "specialization": "{{doctor_specialization_2}}",
                    "email": "{{doctor_email_2}}",
                    "license_number": "{{doctor_license_2}}",
                    "associated_clinic_id": "{{clinic_id_2}}"
                }}
            ],

            "visits": [
                {{
                    "visit_id": "visit_1",
                    "visit_date": "{{visit_date_1}}",
                    "vet_notes": "{{vet_notes_1}}",
                    "temperature": "{{temperature_1}}",
                    "weight": "{{current_visit_weight_1}}",
                    "symptoms": "{{symptoms_1}}",
                    "actions_taken": "{{actions_taken_1}}",
                    "overall_cost": "{{total_cost_1}}",
                    "service": "{{service_category_1}}",
                    "bcs": "{{BCS_1}}",
                    "currency_code": "{{determined_currency_code_1}}",
                    "clinic_id": "{{clinic_id_1}}",
                    "vet_id": "{{vet_id_1}}"
                }},
                {{
                    "visit_id": "visit_2",
                    "visit_date": "{{visit_date_2}}",
                    "vet_notes": "{{vet_notes_2}}",
                    "temperature": "{{temperature_2}}",
                    "weight": "{{current_visit_weight_2}}",
                    "symptoms": "{{symptoms_2}}",
                    "actions_taken": "{{actions_taken_2}}",
                    "overall_cost": "{{total_cost_2}}",
                    "service": "{{service_category_2}}",
                    "bcs": "{{BCS_2}}",
                    "currency_code": "{{determined_currency_code_2}}",
                    "clinic_id": "{{clinic_id_2}}",
                    "vet_id": "{{vet_id_2}}"
                }}
            ],

            "vitals": [
                {{
                "vital_id": "vital_1",
                "visit_id": "{{visit_id_1}}",
                "test": "{{vital_test_1}}",
                "result": "{{vital_result_1}}",
                "recorded_at": "{{vital_date_1}}",
                }},
                {{
                "vital_id": "vital_2",
                "visit_id": "{{visit_id_2}}",
                "test": "{{vital_test_2}}",
                "result": "{{vital_result_2}}",
                "recorded_at": "{{vital_date_2}}"
                }}
            ],

            "preventative_care": [
                {{
                    "preventative_care_id": "preventative_care_1",
                    "visit_id": "{{visit_id_1}}",
                    "care_plan": "{{preventative_care_plan_1}}",
                    "status": "{{preventative_care_status_1}}",
                }},
                {{
                    "preventative_care_id": "preventative_care_2",
                    "visit_id": "{{visit_id_2}}",
                    "care_plan": "{{preventative_care_plan_2}}",
                    "status": "{{preventative_care_status_2}}"
                }}
            ],

            "patient": {{
                "name": "{{patient_name}}",
                "species": "{{species}}",
                "breed": "{{breed}}",
                "sex": "{{sex}}",
                "status": "{{status}}",
                "ids": [
                    {{
                        "id": "{{id}}",
                        "type": "{{id_type}}"
                    }}
                ],
                "color": "{{color}}",
                "dob": "{{dob}}",
                "microchip": "{{microchip}}"
            }},

            "owner": {{
                "name": "{{owner_name}}",
                "phone": "{{owner_phone}}",
                "address": "{{owner_address}}",
                "email": "{{owner_email}}"
            }},
            "other_info": {{
                "details": "{{details}}",
                "medical_history": "{{medical_history}}"
            }},
            "remainders": [
                "{{remainder}}"
            ] if "{{remainders}}" else []
        }}



        **POST-PROCESSING VALIDATION CHECKLIST - CRITICAL FOR visit_id AND REMINDERS**:

        During post-processing, verify each of these items:

        1. **MANDATORY visit_id POPULATION CHECK**:
           - followup array: Check that EVERY entry has visit_id populated
           - invoice array: Check that EVERY entry has visit_id populated  
           - lab_tests array: Check that EVERY entry has visit_id populated
           - reminder array: Check that EVERY entry has visit_id populated
           - treatment_medications array: Check that EVERY entry has visit_id populated
           - treatment_tasks array: Check that EVERY entry has visit_id populated
           - vaccinations array: Check that EVERY entry has visit_id populated
           - pet_weight array: Check that EVERY entry has visit_id populated

        2. **visit_id CONSISTENCY CHECK**:
           - Verify that all visit_id references (visit_1, visit_2, etc.) correspond to actual visit entries
           - Ensure no orphaned visit_id references exist
           - Confirm that visit_id assignments make logical sense based on document content

        3. **CLINIC AND VET ASSOCIATION CHECK**:
           - Verify that each visit has proper clinic_id and vet_id references
           - Ensure clinic_id and vet_id references in other arrays match actual clinic/vet entries
           - Check that vet associations with clinics are logical and consistent

        4. **DATE AND WEIGHT VALIDATION**:
           - Ensure BOTH weight_lbs and weight_kg values are provided for each weight entry
           - Verify that visit dates are in YYYY-MM-DD format and not empty
           - Check that weight recorded_at dates are appropriate

        5. **REMINDER VALIDATION - ENHANCED CRITICAL CHECK**:
           - **MANDATORY**: Perform final comprehensive scan for any missed reminder content
           - Check if reminder array is empty when document contains future care instructions
           - Verify ALL reminder entries have required fields populated:
             * reminder_start_date (MANDATORY - never empty)
             * message (MANDATORY - never empty)
             * reminder_type (MANDATORY - never empty)
             * frequency (MANDATORY - never empty)
             * visit_id (MANDATORY - never empty)
             * is_completed (always false for new extractions)
           - Ensure reminder_start_date and reminder_end_date are in YYYY-MM-DD format
           - Validate reminder_type is one of: "Vaccination", "Check-up", "Medication", "Follow-up", "Preventive Care", "Monitoring", "Testing", "Dental", "Licensing", "Other"
           - Validate frequency is one of: "Once", "Daily", "Weekly", "Monthly", "Annually", "As needed"

        6. **ARRAY FILTERING**:
           - Filter out any empty entries from all arrays
           - Ensure no duplicated information appears in remainders and other fields
           - Remove entries where key required fields are empty

        7. **CONTENT COMPLETENESS CHECK**:
           - Ensure treatment_tasks contains at least one valid entry if medical information exists
           - Ensure lab_tests contains at least one valid entry if diagnostic information exists
           - Ensure visits array contains at least one valid entry if visit information exists
           - Ensure followup array captures ALL follow-up appointments mentioned
           - **Ensure reminder array captures ALL future care instructions, schedules, and recommendations**

        8. **CURRENCY AND SERVICE VALIDATION**:
           - Verify currency_code is populated for each visit based on clinic location or explicit mentions
           - Ensure service categories match predefined options exactly

        **CRITICAL SUCCESS CRITERIA**:
        The extraction is considered successful ONLY if:
        - ALL arrays requiring visit_id have it populated for EVERY entry
        - Visit identification correctly distinguishes actual visits from historical data
        - No phantom visits are created from historical data references
        - All visit_id references are consistent and logical
        - Required fields for critical arrays (visits, treatment_tasks, etc.) are populated when data exists
        - **ALL reminder information is captured in the reminder array with complete field population**
        - **NO future care instructions, schedules, or recommendations are missed in reminder detection**

        The below is the text extracted from medical record document:
        {CURRENT_REPORT}

        (NOTE: - You **must not miss any vaccinations not Test** mentioned in the above text, even if they are historical or scheduled for future dates
               - **Make sure not have any duplicates in vaccinations details in the response json**)
    """
    return prompt_v1