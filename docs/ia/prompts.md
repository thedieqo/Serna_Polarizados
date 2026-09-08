# Prompt Library — Serna Polarizados

> English translation of the supplied Spanish document. Historical execution dates refer to the original tests, not new executions of this translation.

## Status and reading guide

**Documentation update:** September 8, 2026.

This library preserves five recorded tests, P-01 through P-05, performed on September 5, 2026. It includes the original prompts, the available responses or summaries, and review observations.

The original prompts are preserved in Spanish because that is how they were executed. They do not represent five tests in English. The English prompts subsequently executed with Gemini are documented in [pruebas-gemini.md](pruebas-gemini.md).

The responses, priorities and outstanding items from each test describe the project at that time. They do not replace the [current requirements](../requisitos.md). A summarized response is not presented as a complete transcript.

Proposed improvements are not considered executed until a new test exists. No measured token savings are claimed either.

## Historical test index

| ID | Purpose | Recorded tool | Date |
| --- | --- | --- | --- |
| P-01 | Review the scope | Codex | September 5, 2026 |
| P-02 | Draft the vision | Codex | September 5, 2026 |
| P-03 | Compare existing solutions | Codex with web search | September 5, 2026 |
| P-04 | Propose user stories | Codex | September 5, 2026 |
| P-05 | Propose MoSCoW priorities | Codex | September 5, 2026 |

## Subsequent changes to keep in mind

This section updates the context without changing the historical prompts or responses:

- The advisor's interview and the administrator's clarifications were incorporated.
- Recording rolls and offcuts with dimensions in centimeters was agreed. Precision and the cutting procedure remain unresolved.
- Installation details were expanded, and HU-14 was added to discard complete damaged pieces.
- The current document contains 13 active stories. HU-07 remains excluded.
- HU-02 and HU-04 are currently listed as Must. HU-13 retains Must as a reference priority; HU-12 retains Should as a reference priority. HU-14's priority and the review of inventory effort remain pending.
- Acceptance criteria now exist, although HU-05, HU-10 and HU-13 still have incomplete aspects.
- The competitive analysis was updated on September 8 with Odoo 18 references. P-03's Odoo 19 references are preserved as part of the historical record.

Joint reviews with Jonathan, evaluation by another team and subsequent validation with the advisor are not presented as completed.

The records of the five tests follow. Sections titled “Outstanding items”, “Final result” or similar must be read as part of each historical test.

## P-01 — Review the project scope

### Test details

- Date: September 5, 2026.
- Tool: Codex.
- Purpose: separate confirmed rules from pending decisions.
- Status: executed; joint team review pending.

### Prompt used

Act as a requirements analyst for a small academic project.

CONTEXT:
We are two students and are in week 4. Our project is a web system for the two Serna Polarizados branches in Ibagué. Both branches share customer, vehicle and job-history information, but each has its own inventory.

The first version includes registering customers and vehicles, recording jobs with date, branch, service and total value, consulting the history, and recording material receipts and consumption by branch. Consumption must be linked to a job.

TASK:
Review this scope and identify five operating rules that are already confirmed and three decisions we still need to clarify before designing the system.

FORMAT:
Two numbered lists: “Confirmed rules” and “Pending decisions”. Explain each point in one simple sentence.

CONSTRAINTS:
Do not generate code. Do not add payments, invoicing, scheduling, QR or new branches. Do not present your proposals as business decisions. Do not invent measurement units or user permissions.

EXAMPLE:
Confirmed rule: a job's consumption is deducted only from the inventory of the branch where it was performed.
Pending decision: define how to correct consumption recorded by mistake.

### Response obtained

Confirmed rules:

1. The system will cover only the two Serna Polarizados branches in Ibagué.
2. Both branches will share customer, vehicle and job-history information.
3. Each branch will maintain its own material inventory.
4. Each job will be associated with a vehicle and record date, branch, service and total value.
5. Each consumption will be linked to a job and deducted only from the inventory of the branch where it was performed.

Pending decisions:

1. Define material measurement units and how to record fractional quantities.
2. Determine which users may consult, register and modify each type of information.
3. Define how to correct consumption recorded by mistake and adjust the corresponding stock.

### Assisted review observations

What worked:

- Delivered five rules and three pending decisions.
- Used simple sentences.
- Preserved the two-branch scope.
- Distinguished shared information from independent inventory.
- Did not generate code or include excluded modules.

Limitations:

- The prompt does not directly express the relationship between job and vehicle, although that relationship is agreed in the README and conversation.
- Fractional quantities are raised for consideration; they are not yet an approved business rule.

Proposed correction for a future execution:

Add to the context: “Each job belongs to a vehicle and to the branch where it was performed”. This will allow the prompt to be reused without depending on the previous conversation.

This improvement has not yet been executed as a second test.

### Pending human review

Both team members must review these observations and record whether they accept the response or what they change. Jonathan's review and evaluation by another team have not yet been recorded.

## P-02 — Draft the project vision

### Test details

- Date: September 5, 2026.
- Tool: Codex.
- Objective: obtain a brief project vision.
- Status: executed; joint team review pending.

### Prompt used

Act as a software analyst helping two students draft the vision of a small academic project.

CONTEXT:
The project is a web system for the two Serna Polarizados branches in Ibagué. The business currently uses manual records and Excel files.

The first version includes customers, vehicles, completed jobs and inventory. Both branches share customer, vehicle and job-history information, but each manages its own inventory.

A customer may have several vehicles. Each job belongs to a vehicle and to the branch where it was performed, and records date, service and total value. Each material consumption is linked to a job and deducted only from that branch's inventory.

The people involved are administrator, advisor, installer and customer. Permissions are not yet defined, and the customer will not have a self-service portal.

TASK:
Write a brief draft of the project vision explaining the problem, people involved, value proposition and first-version scope.

FORMAT:
Use five sections: Problem, People involved, Value proposition, MVP scope and Exclusions. Maximum 300 words in total.

CONSTRAINTS:
Do not generate code or user stories. Do not invent statistics, measured benefits or permissions. Do not include payments, invoicing, Siigo, scheduling, QR, suppliers, automatic alerts or additional branches in the MVP. Distinguish recording a job's value from managing its payment.

EXAMPLE:
Value proposition: consult a vehicle's history from either branch while keeping each branch's inventory separate.

### Response obtained

#### Problem

Serna Polarizados uses manual records and Excel files. The project aims to organize customer, vehicle, job and material information to facilitate consultation between the two Ibagué branches.

#### People involved

Administrator, advisor, installer and customer. Their permissions and responsibilities within the system remain to be defined. The customer provides information but will not have a self-service portal in the first version.

#### Value proposition

Centralize customer, vehicle and job-history information for consultation from both branches, maintaining independent inventory per branch and linking consumed materials to each job.

#### MVP scope

- Register customers and associate several vehicles with the same customer.
- Record jobs linked to a vehicle and a branch, including date, service and total value.
- Consult job history from both branches.
- Record materials, receipts, consumption and stock by branch.
- Link each consumption to a job and deduct it only from the inventory of the branch where it was performed.

The total value describes the job amount; recording it does not include managing or checking its payment.

#### Exclusions

The first version does not include payment management, invoicing, Siigo integration, appointment scheduling, QR registration, supplier management, automatic alerts or additional branches.

Material measurement units and user permissions will be clarified during requirements analysis.

### Assisted review comments

- The response included the five requested sections and did not exceed 300 words.
- Preserved the two-branch scope with separate inventories.
- Distinguished recording job value from managing payment.
- Did not invent permissions or measured results.
- Included receipts and stock, previously agreed but not detailed in this prompt.

### Proposed improvement

Add to the context: “Inventory includes registering materials, receipts, consumption and consulting stock”.

This improvement would make the prompt more precise. That new version has not yet been tested.

### Pending human review

Both team members must read the result and record their observations. The comments above were prepared with AI assistance and do not amount to Jonathan's review.

## P-03 — Compare existing solutions

### Test details

- Date: September 5, 2026.
- Tool: Codex with web search.
- Objective: compare three systems using official sources.
- Status: executed; joint team review pending.

### Prompt used

Act as a software analyst for a small academic project.

CONTEXT:
We are developing Serna Polarizados for two branches in Ibagué. The scope includes customers, vehicles, completed jobs and independent inventory per branch. Both branches share job history. Each material consumption must be linked to a job and deducted from the corresponding branch.

TASK:
Consult official Shopmonkey, AutoLeap and Odoo sources and compare their functions relevant to this project. At the end, identify three lessons we can apply without expanding our scope.

FORMAT:
A table with three rows and these columns: System, Verified functions, Usefulness for Serna and Aspects pending verification. Then provide a list of three lessons. Include links to the sources used.

CONSTRAINTS:
Do not invent functions, prices or tests performed. Distinguish published information from your interpretations. If you cannot verify something, write “Not verified”. Do not claim our project is superior. Do not add payments, invoicing, scheduling, QR or other functions to the MVP.

EXAMPLE:
Aspect pending verification: check whether the system allows recording fractional consumption of window-film material in meters.

### Summary of the response obtained

Official sources were consulted. No functional tests of the systems were performed.

- Shopmonkey: documents customer registration, vehicle association, service history and inventory tools related to jobs.
- AutoLeap: documents tracking parts by job, stock by location and inventory management across multiple branches.
- Odoo: documents contact registration and stock organization through warehouses and locations.
- Specific aspects such as fractional window-film consumption and the configuration required to reproduce Serna's entire workflow remained unverified.

The three proposed lessons were:

1. Link each job to a vehicle and each vehicle to its customer.
2. Identify the branch affected by each receipt or consumption.
3. Preserve the material and quantity used per job, defining the measurement units first.

### Sources consulted

- Shopmonkey, customers and vehicles:
  https://support.shopmonkey.io/hc/en-us/articles/38744260861204-Lists-Page
- Shopmonkey, inventory:
  https://www.shopmonkey.io/demo-inventory-management
- AutoLeap, inventory:
  https://autoleap.com/features/inventory/
- Odoo 19, contacts:
  https://www.odoo.com/documentation/19.0/applications/essentials/contacts.html
- Odoo 19, inventory organization:
  https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management.html

### Assisted review comments

What worked:

- Delivered a table with three systems and four columns.
- Included three lessons related to the scope.
- Used official sources and separated documented functions from interpretations.
- Identified what could not be verified.
- Did not compare prices or claim Serna was superior.

Limitations:

- The review was documentary; it does not demonstrate practical operation.
- Did not confirm all important aspects for Serna, such as fractional material consumption.
- The Odoo sources correspond to version 19; the earlier competitive analysis cited versions 17 and 18.

Corrections and follow-up:

The response was not modified during this test. Reviewing whether to update the competitive analysis references to use a single Odoo version remains pending.

No second execution of the prompt was performed.

### Pending human review

The team members must open the sources, review the claims and record their observations. Assisted review does not replace team review.

## P-04 — Propose user stories

### Test details

- Date: September 5, 2026.
- Tool: Codex.
- Objective: propose user stories for the agreed scope.
- Status: executed and reviewed with one team member; review with Jonathan pending.

### Prompt used

Act as a requirements analyst for a small academic project.

CONTEXT:
Serna Polarizados needs a system for its two branches in Ibagué. Both share customers, vehicles and job history, but each branch has independent inventory.

The scope includes:

- Registering and consulting customers with name, identification document and contact information.
- Registering vehicles associated with customers and searching for them by plate.
- Recording jobs associated with a vehicle and a branch, with date, service and total value.
- Consulting job history from both branches.
- Registering materials, receipts and consumption, and consulting stock by branch.
- Linking each consumption to a job and deducting it from that branch's inventory.

The identified profiles are administrator, advisor and installer. Their specific permissions remain to be defined.

TASK:
Propose 12 user stories for this scope. Each story must express a specific need and be reviewable separately.

FORMAT:
A numbered list from HU-01 through HU-12. Use the following in each:
“As a [profile], I want [action] so that [benefit]”.
Then include up to three relevant questions for reviewing the stories.

CONSTRAINTS:
Do not generate code. Do not add payments, invoicing, scheduling, QR, suppliers, automatic alerts or new branches. Recording a job's value does not mean managing its payment. Do not invent measurement units. Profile assignments are proposals for validation, not confirmed permission decisions. Do not artificially split the same need to reach 12 stories.

EXAMPLE:
As an advisor, I want to consult a vehicle's history by its plate so that I can see previous jobs before serving the customer.

### Summary of the initial response

The AI proposed these 12 stories:

- HU-01: register a customer.
- HU-02: consult a customer.
- HU-03: register a vehicle.
- HU-04: consult a vehicle.
- HU-05: record a job.
- HU-06: consult vehicle history.
- HU-07: consult jobs by branch and period.
- HU-08: register a material.
- HU-09: record a material receipt.
- HU-10: record material consumption.
- HU-11: consult stock.
- HU-12: consult a job's materials.

It also asked about permissions, measurement units and the need for HU-07.

### What worked

- Delivered 12 stories with profile, action and benefit.
- Preserved inventory separation by branch.
- Linked consumption to jobs.
- Presented profiles as proposals for review.
- Asked questions that elicited user decisions.

### What did not work

HU-07's query by branch and period was not necessary for the first version. The AI proposal required a scope correction.

### Human review and corrections

One team member reviewed the stories and:

1. Accepted the stories except HU-07.
2. Excluded HU-07 because it was unnecessary.
3. Confirmed that the advisor and administrator would be able to register and consult the information mentioned.
4. Confirmed that the installer uses the platform and provides data about consumed materials.

The AI then proposed:

HU-13: As an administrator, I want to correct material consumption recorded by mistake, preserving a record of the adjustment, so that the branch's stock reflects actual consumption.

The user explicitly confirmed that the administrator must be able to make that correction.

### Final result

Twelve stories were accepted: HU-01 through HU-06 and HU-08 through HU-13.

HU-07 is preserved as excluded to maintain the change record.

The complete, reviewed stories are available in:

[View requirements](../requisitos.md)

### Outstanding items

- Clarify measurement units and quantity precision: identifying the installer as the source does not yet resolve this decision.
- Review the stories with Jonathan.
- Assign MoSCoW priorities.
- Write Gherkin acceptance criteria for Must stories.

## P-05 — Prioritize stories with MoSCoW

### Test details

- Date: September 5, 2026.
- Tool: Codex.
- Objective: propose priorities based on the main demonstration.
- Status: executed; prioritization pending team review.

### Prompt used

Act as a requirements analyst for a small academic project.

CONTEXT:
We are two students and will develop a system for the two Serna Polarizados branches in Ibagué. Both share customers, vehicles and job history, but each branch maintains its own inventory.

The main demonstration must allow registering a customer and their vehicle, recording a material receipt, recording a job, linking consumption to it, and verifying that only the corresponding branch's inventory decreases. The vehicle's history must be accessible from both branches.

These are the accepted stories:

- HU-01: register a customer.
- HU-02: consult a customer by identification document.
- HU-03: register a vehicle associated with a customer.
- HU-04: consult a vehicle by plate.
- HU-05: record a job with vehicle, branch, date, service and total value.
- HU-06: consult vehicle history from both branches.
- HU-08: register a material and its measurement unit.
- HU-09: record a material receipt by branch.
- HU-10: record consumption associated with a job and deduct it from the corresponding branch.
- HU-11: consult stock by branch.
- HU-12: consult materials and quantities consumed in a job.
- HU-13: allow the administrator to correct erroneous consumption, preserving a record of the adjustment.

HU-07, consulting jobs by branch and period, was explicitly excluded.

TASK:
Propose a MoSCoW priority for each accepted story and briefly explain the reason. Consider the dependencies needed to complete the main demonstration.

FORMAT:
A table with the columns ID, Story, Priority and Rationale. Then explain in simple language what could be postponed and its effect. Record HU-07 separately as out of scope.

CONSTRAINTS:
Prioritization is a proposal pending team review. Do not change identifiers or add functions. Do not reintroduce HU-07. Do not invent mandatory percentages for each category: it is fine if a category remains empty. Distinguish what is essential for the main flow to work from what can wait. Do not generate code or Gherkin criteria yet.

EXAMPLE:
HU-09 | Record a material receipt | Must | Provides stock to demonstrate material consumption.

### Summary of the response obtained

The AI proposed:

- Must: HU-01, HU-03, HU-05, HU-06, HU-08, HU-09, HU-10 and HU-11.
- Should: HU-02, HU-04, HU-12 and HU-13.
- Could: none.
- Won’t: HU-07, previously excluded.

General rationale:

The Must stories allow completing the flow from customer registration through inventory verification and cross-branch history consultation.

Searches by identification document and plate were proposed as Should, provided the main functions allow customers and vehicles to be selected correctly.

The detailed query of materials by job was proposed as Should, while keeping the relationship between consumption and job mandatory.

Consumption correction was proposed as Should for the academic demonstration, noting that it should be completed before using the system in a real operation.

### Assisted review comments

What worked:

- Classified the twelve accepted stories.
- Kept HU-07 out of scope.
- Justified priorities based on the demonstration.
- Did not force the use of every category.
- Explained the effects of postponing functions.
- Did not generate code or Gherkin criteria.

Limitations:

- Postponing HU-02 and HU-04 depends on a selection mechanism that still needs to be detailed.
- The importance of correcting consumption must be reviewed with the team; its priority was not confirmed by the user.
- The classification targeted an academic demonstration, not a complete real operation.

### Corrections and pending decisions

The proposed classification has not yet been modified or approved.

The team must decide:

1. Whether searches by identification document and plate should be Must.
2. Whether consumption correction should be Must.
3. Whether it accepts the remaining priorities.

### Pending human review

Executing this prompt does not amount to approving its results.

Joint review with Jonathan and evaluation by another team remain pending.

## Current follow-up

- Preserve original prompts and results without replacing them with translations presented as past tests.
- For new executions, use instructions in English and request the response in Spanish, following the instruction reported by the student.
- Record any new version separately, along with its actual date, tool, result and corrections.
- Review the results with Jonathan and record only reviews that actually took place.
- Complete the prompt evaluation and exchange requested in class.
- Consult the current requirements for the current scope and priorities.

Having five records does not, by itself, establish that the entire submission has been reviewed or that a requirement for five executions in English has been met. Prompt tests are not software functionality tests either.
