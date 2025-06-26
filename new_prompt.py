CURRENCY_PROMPT = """
        - For the "currency_code" field in each visit, follow this priority order:
          1. **Explicit Currency Mention**: If currency symbols or codes are explicitly mentioned in the document for 
               that visit (e.g., $, USD, €, EUR, £, GBP, etc.), use that currency code
          2. **Invoice/Payment Sections**: Check invoice, payment, or billing sections for currency indicators related to that visit
          3. **Clinic Address-Based Currency**: If no explicit currency is mentioned, determine based on the SPECIFIC clinic address for that visit:
             - **United States**: USD
             - **Canada**: CAD
             - **United Kingdom**: GBP
             - **European Union countries**: EUR (Germany, France, Italy, Spain, Netherlands, Belgium, Austria, Portugal, 
                                                  Ireland, Finland, Greece, Luxembourg, Slovenia, Slovakia, Estonia, Latvia, Lithuania, Malta, Cyprus)
             - **Australia**: AUD
             - **New Zealand**: NZD
             - **Japan**: JPY
             - **India**: INR
             - **China**: CNY
             - **South Korea**: KRW
             - **Brazil**: BRL
             - **Mexico**: MXN
             - **Switzerland**: CHF
             - **Sweden**: SEK
             - **Norway**: NOK
             - **Denmark**: DKK
             - **Poland**: PLN
             - **Czech Republic**: CZK
             - **Hungary**: HUF
             - **Romania**: RON
             - **Bulgaria**: BGN
             - **Croatia**: HRK
             - **Israel**: ILS
             - **South Africa**: ZAR
             - **Russia**: RUB
             - **Turkey**: TRY
             - **Singapore**: SGD
             - **Hong Kong**: HKD
             - **Thailand**: THB
             - **Malaysia**: MYR
             - **Indonesia**: IDR
             - **Philippines**: PHP
             - **Vietnam**: VND
             - **Argentina**: ARS
             - **Chile**: CLP
             - **Colombia**: COP
             - **Peru**: PEN
             - **Uruguay**: UYU
             - **Paraguay**: PYG
             - **Bolivia**: BOB
             - **Ecuador**: USD
             - **Venezuela**: VES
          4. **Default**: If clinic address is unclear or not provided, use "USD" as default
          5. **Validation**: Ensure currency codes are in standard 3-letter ISO format (e.g., USD, EUR, GBP)
"""

DOCUMENT_TYPE = """     
                The below are the document types uploaded via OCR:
                (Multiple documents may be uploaded through OCR, populate the document_type values 
                for the 'documents' key in the JSON accordingly):       
                    - Services - Dog License Renewal
                    - Payment for Services
                    - Rabies Vaccination
                    - Vaccination Certificate
                    - Rabies Vaccination Certificate
                    - Dog Licensing
                    - Vaccination Certification
                    - License Renewal Notice
                    - Health Examination
                    - Order Confirmation
                    - Payment Receipt
                    - Examination and Vaccinations
                    - Invoice for Pet Services
                    - Wellness Exam and Vaccination
                    - Lab Results Notification
                    - Invoice for Veterinary Services
                    - Invoice for Services
                    - Examination and Vaccination
                    - Payment Received
                    - Examination and Treatments
                    - Examination and Services
                    - Examination and Medications
                    - Recheck Exam and Medications
                    - Examination and Laboratory Services
                    - Dog Spay Surgery and Medications
                    - Vaccination and Consultation
                    - Vaccination and Medical Fee
            """

JSON_STRUCTURE = f"""
            {{
               "owner": {{
                   "name": "{{owner_name}}",
                   "phone": "{{owner_phone}}",
                   "address": "{{owner_address}}",
                   "email": "{{owner_email}}"
               }},

               "patient": {{
                   "name": "{{patient_name}}",
                   "species": "{{species}}",
                   "breed": "{{breed}}",
                   "sex": "{{sex}}",
                   "status": "{{status}}",
                   "ids": [
                       {{
                           "type": "{{id_type}}"
                           "id": "{{id}}",     
                       }}
                   ],
                   "color": "{{color}}",
                   "dob": "{{dob}}",
                   "microchip": "{{microchip}}"
               }},

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
                       "vet_id": "{{vet_id_1}}",
                       "reason_for_visit": "{{reason_for_visit_1}}",
                       "history": "{{history_1}}",
                       "assessment": "{{assessment_1}}",
                       "plan": "{{plan_1}}"
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
                   "recorded_at": "{{vital_date_1}}"
                   }},
                   {{
                   "vital_id": "vital_2",
                   "visit_id": "{{visit_id_2}}",
                   "test": "{{vital_test_2}}",
                   "result": "{{vital_result_2}}",
                   "recorded_at": "{{vital_date_2}}"
                   }}
               ],

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

               "vaccinations": [
                   {{
                       "vaccine_name": "{{vaccine_name_1}}",
                       "date_administered": "{{vaccine_date_administered_1}}",
                       "due_date": "{{vaccine_due_date_1}}",
                       "clinic_id": "{{clinic_id_1}}",
                       "vet_id": "{{vet_id_1}}",
                       "visit_id": "{{visit_id_1}}",
                       "status": "{{status_1}}"
                   }},
                   {{
                       "vaccine_name": "{{vaccine_name_2}}",
                       "date_administered": "{{vaccine_date_administered_2}}",
                       "due_date": "{{vaccine_due_date_2}}",
                       "clinic_id": "{{clinic_id_2}}",
                       "vet_id": "{{vet_id_2}}",
                       "visit_id": "{{visit_id_2}}",
                       "status": "{{status_2}}"
                   }}
               ],

               "preventative_care": [
                   {{
                       "preventative_care_id": "preventative_care_1",
                       "visit_id": "{{visit_id_1}}",
                       "care_plan": "{{preventative_care_plan_1}}",
                       "status": "{{preventative_care_status_1}}"
                   }},
                   {{
                       "preventative_care_id": "preventative_care_2",
                       "visit_id": "{{visit_id_2}}",
                       "care_plan": "{{preventative_care_plan_2}}",
                       "status": "{{preventative_care_status_2}}"
                   }}
               ],

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

               "documents": {{
                   "document_type": "{{document_type}}"
               }},

               "other_info": {{
                   "details": "{{details}}",
                   "medical_history": "{{medical_history}}"
               }},

               "remainders": [
                   "{{remainder}}"
               ] if "{{remainders}}" else []
            }}

        (⚠️ IMPORTANT: This data will be stored in a structured database. 
        Therefore, extraction must be meticulous, accurate, and fully capture the medical details. 
        Prioritize accuracy, completeness and Do not skip or generalize information.)
"""


def get_prompt():
    prompt_v6 = """
            You are a data annotator tasked with extracting all relevant medical and contextual 
            information from veterinary documents extracted by OCR (e.g., clinical notes, prescriptions, diagnostics, lab summaries).

            **Important Note**: The document contains both the pet owner and clinic information. Some documents may contain 
            information about MULTIPLE visits at DIFFERENT clinics. Ensure you correctly differentiate between them and 
            extract ALL clinic information found.

            ## GOAL: You need create a JSON file with the below keys (Each key represents either JSON or array of JSON):
                └── 1) owner
                    └── 2) patient (Pet)
                        └── 3) clinics (multiple clinics possible)
                            └── 4) vets (veterinarian)
                                └── 5) visits (multiple visits possible)
                                    ├── 6) vitals (BP, Heart Rate etc.)
                                    ├── 7) pet_weight
                                    ├── 8) lab_tests
                                    ├── 9) pet_disease
                                    ├── 10) treatment_tasks
                                    ├── 11) treatment_medications
                                    ├── 12) vaccinations
                                    ├── 13) preventative_care
                                    ├── 14) invoice
                                    └── 15) followup
                                        └── 16) reminder
                                            └── 17) documents
                                                └── 18) other_info
                                                    └── 19) remainders

            ## CRITICAL INFORMATION EXTRACTION DISTINCTIONS

                **Distinguishing Owner vs Multiple Clinics Information - CRITICAL**:
                - Pay careful attention to document sections with explicit labels like "VETERINARY CLINIC", "OWNER OF ANIMAL", "CLIENT", "PET OWNER", etc.
                - Multiple clinics may appear in: different sections, referral information, historical visits, emergency visits
                - **NEVER use clinic information as owner information when owner data is not provided (and vice versa)**
                - Look for explicit section headers or labels that clearly indicate which information belongs to which entity
                - If owner information fields are not present in the document, leave them as empty strings
                - Create separate clinic entries for each distinct clinic mentioned

                **VISIT IDENTIFICATION AND EXTRACTION - MOST CRITICAL SECTION FOR visit_id ASSIGNMENT**:

                **STEP 1: IDENTIFY ALL ACTUAL VISITS**
                - Extract ALL **ACTUAL** visits mentioned with documented examination/appointment including:
                  * Specific date when pet physically visited clinic
                  * Clinical notes, examination findings, or veterinary interaction
                  * Services provided, treatments administered, or assessments made

                **STEP 2: DISTINGUISH ACTUAL VISITS FROM HISTORICAL DATA**
                - **ACTUAL VISITS** = Documented appointments with vet interaction and clinical notes
                - **HISTORICAL DATA** = Previous information referenced during visit but not separate appointments
                - Examples of HISTORICAL DATA (DO NOT create separate visits): "Previous weight was 45 lbs", "Last vaccination 6 months ago"

                **STEP 3: CREATE UNIQUE visit_id FOR EACH ACTUAL VISIT**
                - Assign sequential visit_ids: "visit_1", "visit_2", etc.
                - Each ACTUAL visit gets exactly ONE unique visit_id
                - NEVER create visit_ids for historical data references

                **STEP 4: ASSOCIATE ALL DATA WITH CORRECT visit_id**
                - Every piece of data must be associated with the visit where it was DOCUMENTED/RECORDED
                - For current visit data: Use current visit's visit_id
                - For historical data mentioned during visit: Use CURRENT visit's visit_id (where referenced)

            ## TYPE DEFINITIONS AND EXTRACTION LOGIC:
                (Go through the below 19 instructions for the 19 fields' extraction logics and follow every nuances)

                **1) owner** [Pet Owner Information]:
                **TYPE:** JSON.
                **EXTRACTION LOGIC:**
                - `Pet Owner name`: Person who owns the pet
                - `Pet Owner phone`: Phone number associated with pet's owner
                - `Pet Owner address`: Home address of pet owner
                - `Pet Owner email`: Email address of pet owner (if available)

                **2) patient** [Pet Information]:
                **TYPE:** JSON.
                **EXTRACTION LOGIC:**
                - Extract: name, species, breed, sex, status, color, dob, microchip
                - `ids` key represents array of JSON, populated by 'id' (**A number or alphanumeric**) and 'type' from clinic records
                - Here 'id' represents the unique ID of the patient (i.e: Pet), don't confuse with microchip ID or any other ID.
                - Multiple ids may be present so populate array accordingly

                **3) clinics** [Multiple clinics possible]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Assign `clinic_id` to differentiate multiple clinics (clinic_1, clinic_2, etc.)
                - Extract clinic info: name, email, phone, address
                - Do NOT confuse with owner's info while extracting clinic details

                **4) vets** [Multiple veterinarians possible]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Assign `vet_id` (vet_1, vet_2, etc.) for each JSON in array
                - Extract vet info: name, phone, specialization, email, license_number
                - Include `associated_clinic_id` to link vet with their clinic
                - **CRITICAL**: ONLY return veterinarian's personal/direct phone number explicitly linked to veterinarian
                - NEVER include clinic or pet owner phone numbers in vet phone field

                **5) visits** [Multiple visits possible]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Assign sequential `visit_id` (visit_1, visit_2, etc.) for each ACTUAL documented visit
                - Extract visit_date, vet_notes, temperature, weight, symptoms, actions_taken, overall_cost
                - Fields like 'reason_for_visit', 'history', 'assessment', 'plan' can be populated if available in the document
                - Include service category, BCS (Body Condition Score), currency_code appropriately
                - Associate with `clinic_id` and `vet_id` references
                - **Date Priority**: Look for explicit visit dates, then document dates, NEVER leave visit_date empty


                **6) vitals** [Vital signs measurements]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Assign `vital_id` (vital_1, vital_2, etc.) for each vital measurement
                - Extract test type (BP, heart rate, temperature, respiratory rate) and result values
                - Include `recorded_at` date and associate with `visit_id`
                (**NOTE: This is mandatory, include the vitals if given**)

                **7) pet_weight** [Weight measurements]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract ALL weight mentions with both `weight_lbs` and `weight_kg` (convert if needed)
                - Use conversion: weight_kg = weight_lbs * 0.453592 or weight_lbs = weight_kg * 2.20462
                - Include `recorded_at` date and associate with `visit_id`
                - Create separate entries for each weight measurement found
                - **CRITICAL**: Each weight entry MUST have visit_id populated

                **8) lab_tests** [Diagnostic tests]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `test_name`, `test_result`, `test_date` for all laboratory work
                - Include `purpose`, `ordered_date`, `expected_date`, `status`
                - Cover blood work, urine tests, fecal exams, screening tests, imaging
                - Associate with `clinic_id`, `vet_id`, and `visit_id`
                - **CRITICAL**: Each lab test entry MUST have visit_id populated

                **9) pet_disease** [Medical conditions]:
                **TYPE:** JSON.
                **EXTRACTION LOGIC:**
                - Extract `allergies` and ongoing medical conditions
                - Focus on chronic, recurring, or significant health issues

                **10) treatment_tasks** [Diagnoses and treatments]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `condition`, `diagnosis`, `treatment_plan` for each treatment provided
                - Include `follow_up_required` (Yes/No), `treatment_date`
                - Associate with `clinic_id`, `vet_id`, and `visit_id`
                - **CRITICAL**: Each treatment task entry MUST have visit_id populated

                **11) treatment_medications** [Prescribed medicines]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `medication_name`, `dosage`, `frequency`, `duration`
                - Include `prescribed_date` and `notes` for additional instructions
                - Associate with `clinic_id`, `vet_id`, and `visit_id`
                - **CRITICAL**: Each medication entry MUST have visit_id populated

                **12) vaccinations** [Vaccine records]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC (Give attention to detail, accuracy must):**
                - Extract `vaccine_name`, `date_administered`, `due_date` (**Date must be accurate, extract carefully**)
                - Include both historical vaccines and future scheduled doses (i.e: all the vaccines)
                - Populate 'status' as completed or scheduled based on the current date (i.e: document issued date).
                - Associate with `clinic_id`, `vet_id`, and `visit_id`
                - **CRITICAL**: Each vaccination entry MUST have visit_id populated
                (NOTE: Do not include lab tests, wellness exams etc. in vaccine details, interpret future date by considering the 
                       document issued date as current date)

                **13) preventative_care** [Preventive measures]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Assign `preventative_care_id` (preventative_care_1, etc.) for each entry
                - Extract `care_plan` and `status` for preventive treatments
                - Include cares like heartworm prevention, flea/tick control, dental care plans, wellness care etc.
                - Associate with `visit_id`
                (**NOTE: This is critical, must include if given**)

                **14) invoice** [Billing information]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `items`, `item_type`, `quantity`, `unit_price`, `total_amount`
                - Include `currency` code and associate with `visit_id`
                - Create separate entries for each billed service, medication, procedure, or supply
                - **CRITICAL**: Each invoice entry MUST have visit_id populated

                **15) followup** [Future appointments]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `follow_up_date`, `purpose`, `vet_assigned` (if specified)
                - Calculate `status` (Scheduled/Overdue/Completed based on document's issued date i.e: medical report)
                - Determine `category` (Vaccination, Wellness Check, Treatment Follow-up, etc.)
                - Include `activity`, `source` (vet_record), associate with `clinic_id` and `visit_id`
                - **CRITICAL**: Each followup entry MUST have visit_id populated
                (NOTE: Interpret the future date from the document issue date.)

                **16) reminder** [Care reminders and alerts]:
                **TYPE:** Array of JSON.
                **EXTRACTION LOGIC:**
                - Extract `reminder_start_date`, `reminder_end_date`, `message`
                - Include `reminder_type` (Vaccination, Check-up, Medication, Follow-up, Preventive Care, 
                                           Monitoring, Testing, Dental, Licensing, Other)
                - Set `frequency` (Once, Daily, Weekly, Monthly, Annually, As needed)
                - Set `is_completed` to false, associate with `visit_id`
                - **ENHANCED REMINDER DETECTION**: Look for vaccination schedules, follow-up recommendations, medication 
                                                   reminders, routine check-ups, conditional reminders, 
                                                   monitoring instructions, preventive care schedules
                - **CRITICAL**: Each reminder entry MUST have 'visit_id' populated and ALL required fields completed
                  (NOTE: Interpret future date by considering the document issued date as current date, and 
                         add the future plans like vaccinations, tests etc. to reminders)

                **17) documents** [Document metadata]:
                **TYPE:** JSON.
                **EXTRACTION LOGIC:**
                - Extract the `document_type` by recognizing the key words or document nature 
                  like Visit Report, Invoice, Payment Receipt, Medical Record, Prescription etc.

                **18) other_info** [Additional clinical information]:
                **TYPE:** JSON.
                **EXTRACTION LOGIC:**
                - Extract `details` and `medical_history` not captured elsewhere

                **19) remainders** [Unprocessed content]:
                **TYPE:** Array of strings.
                **EXTRACTION LOGIC:**
                - Include ONLY text not captured in other structured fields
                - Avoid duplication with already processed content
                - **TRACKING PROCESSED CONTENT**: Mark text as processed during extraction, only add unprocessed content to remainders

            ## SERVICE CATEGORIZATION:
                The "service" field for each visit must be categorized into one of these predefined categories:
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

            ## CURRENCY CODE DETERMINATION:

             {CURRENCY_PROMPT}

            ## Return the JSON in the following format, by considering the extraction logics and nuances):

             {JSON_STRUCTURE}

            ## The below are the document types uploaded via OCR:

             {DOCUMENT_TYPE}

            **CRITICAL VALIDATION RULES:**
            - **MANDATORY visit_id:** ALL arrays requiring visit_id MUST have it populated
            - **Distinguish ACTUAL visits from historical data references**
            - **Convert weights between lbs/kg when needed**
            - **Use YYYY-MM-DD date format throughout**
            - **Associate all data with correct clinic_id, vet_id, and visit_id references**
            - **Do not hallucinate, Just give empty str "" for missing data for a field (only if it is missing)**

            # POST-PROCESSING VALIDATION CHECKLIST (**Do not skip**):

                STEP 1. **MANDATORY visit_id POPULATION**
                **ALL** entries in the below arrays MUST have visit_id populated:
                - followup, invoice, lab_tests, reminder, treatment_medications, treatment_tasks, vaccinations, pet_weight

                STEP 2. **visit_id CONSISTENCY**
                - All visit_id references (visit_1, visit_2, etc.) must correspond to actual visit entries
                - No orphaned visit_id references
                - Logical visit_id assignments based on document content

                STEP 3. **CLINIC/VET ASSOCIATIONS**
                - Each visit requires valid clinic_id and vet_id references
                - Cross-reference consistency between visits and other arrays
                - Logical vet-clinic associations
                - Ensure the correct email ID extraction.

                STEP 4. **DATE/WEIGHT VALIDATION**
                - **Both** weight_lbs and weight_kg required for each weight entry
                - Visit dates in YYYY-MM-DD format (not empty)
                - Strictly give the accurate dates for vaccinations accordingly
                - Appropriate weight recorded_at dates
                (NOTE: Since the cols were extracted the OCR, in some cases col structure will mis align)

                    SINGLE SHOT EXAMPLE:
                        | Performed   | Due Date    |
                        |-------------|-------------|
                        | 06/16/2020  | 06/16/2021  |
                        | 06/16/2020  | 06/16/2021  |
                        | 07/15/2020  | 07/15/2021  |
                        | 06/16/2020  | 06/16/2022  |
                        | 01/18/2023  | 01/18/2024  |
                        | 02/15/2023  | 02/15/2024  |

                    The above is the actual table, but OCR extracted like the below structure:

                        Performed
                        Due Date
                        06/16/2020
                        06/16/2020
                        06/16/2021
                        06/16/2021
                        07/15/2020
                        07/15/2021
                        06/16/2020
                        06/16/2022
                        01/18/2023
                        01/18/2024
                        02/15/2023
                        02/15/2024

                    So you must interpret the structure accordingly.


                STEP 5. **REMINDER VALIDATION - ENHANCED CRITICAL**
                - **MANDATORY**: Final comprehensive scan for ANY missed reminder content
                - Check empty reminder array when document contains future care instructions
                - **ALL** reminder entries require complete field population (If reminder exists check for below fields):
                      * reminder_start_date (MANDATORY - never empty)
                      * message (MANDATORY - never empty)
                      * reminder_type (MANDATORY - never empty)
                      * frequency (MANDATORY - never empty)
                      * visit_id (MANDATORY - never empty)
                      * is_completed (always false for new extractions)
                - Dates in YYYY-MM-DD format
                - reminder_type: "Vaccination", "Check-up", "Medication", "Follow-up", "Preventive Care", 
                                 "Monitoring", "Testing", "Dental", "Licensing", "Other"
                - frequency: "Once", "Daily", "Weekly", "Monthly", "Annually", "As needed"

                STEP 6. **ARRAY FILTERING**
                - Remove empty entries from all arrays
                - No duplicated information in remainders and other fields
                - Remove entries with empty required fields

                STEP 7. **CONTENT COMPLETENESS**
                - treatment_tasks: At least one valid entry if medical information exists
                - lab_tests: At least one valid entry if diagnostic information exists
                - visits: At least one valid entry if visit information exists
                - followup: Capture ALL follow-up appointments mentioned
                - **reminder: Capture ALL future care instructions, schedules, and recommendations**

                STEP 8. **CURRENCY/SERVICE VALIDATION**
                - currency_code populated (with 3 letter ISO standard) for each visit based on 
                  clinic location or explicit mentions
                - Service categories match predefined options exactly

                ## SUCCESS CRITERIA
                **Extraction succeeds ONLY if:**
                - ALL arrays requiring visit_id have it populated for EVERY entry
                - Visit identification correctly distinguishes actual visits from historical data
                - No phantom visits created from historical references
                - All visit_id references are consistent and logical
                - Required fields populated when data exists
                - **ALL reminder information captured with complete field population**
                - **NO future care instructions, schedules, or recommendations missed**

            The below is the text extracted (by OCR) from medical record document:

            {CURRENT_REPORT}

            (NOTE: - You **must not miss any critical medical report like vaccinations and its accurate date, tests, etc**, 
                     even if they are historical or scheduled for future dates.
                   - Document were uploaded via OCR. The alignment and structure follow raw OCR output, so interpret 
                     columns, dates, and other critical fields intuitively)
    """

    return prompt_v6


