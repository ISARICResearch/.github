# ISARIC Data Tools

## Introduction

Clinical data are the cornerstone of an evidence-based outbreak response, impacting decisions at both clinical and policy levels. Rapidly identifying case definitions, outcome rates, and risk factors is crucial for managing novel infections and unexpected epidemiological shifts. Outbreak response from a data perspective includes three critical elements:

1. **Collection**: This process relies on the availability and time of frontline healthcare workers and research staff, which are especially limited in low-resource settings where Electronic Health Records (EHR) are scarce and disease outbreaks are frequent.
2. **Curation**: Maintaining high data quality and consistency is crucial, especially during outbreaks where discrepancies and inconsistent data collection methods can compromise integrity.
3. **Analysis**: Relevant questions must be quickly answered to guide outbreak response. A lack of standardized analysis protocols and limited analytical resources can restrict the ability to quickly generate actionable insights.

ISARIC has developed three open-access tools to address these requirements.

![plot](https://github.com/ISARICResearch/.github/blob/main/profile/diagram.png)

## Tools

### 1. Analysis and Research Compendium (ARC)

ARC is a comprehensive machine-readable document in CSV format, designed for use in Clinical Report Forms (CRFs) during disease outbreaks. It includes a library of questions covering demographics, comorbidities, symptoms, medications, and outcomes. Each question is based on a standardized schema, has specific definitions mapped to controlled terminologies, and has built-in quality control. ARC is openly accessible, with version control via GitHub ensuring document integrity and collaboration.

See [ARC](https://github.com/ISARICResearch/DataPlatform/tree/main/ARCH) to know more about out library of CRF questions.

### 2. BioResearch Integrated Data Tool GEnerator (BRIDGE)

BRIDGE is a web-based application designed to operationalize ARC and edit any ISARIC CRF and tailor it to oubreaks particular context. By selecting and customizing clinical questions and ensuring necessary data points for each, BRIDGE automates the creation of Case Report Forms (CRFs) for each disease and specific research context. It generates the data dictionary and XML needed to create a REDCap database for capturing data in the ARC structure. Additionally, it produces paper-like versions of the CRFs and completion guides.

See [BRIDGE](https://isaric-bridge.replit.app/) to easily build CRFs that suit your objectives, with an automated completion guide, REDCap data dictionary, and REDCap XML to launch your own database that corresponds with the CRF. Aditionally see [BRIDGE GitHub](https://github.com/ISARICResearch/DataPlatform/tree/main/BRIDGE) to check the code. 

### 3. Visual Evidence & Research Tool for Exploration (VERTEX)

VERTEX is a web-based application designed to present graphs and tables based on relevant research questions that need to be quickly answered during an outbreak. VERTEX uses reproducible analytical pipelines. Currently, we have pipelines for identifying the spectrum of clinical features in a disease and determining risk factors for patient outcomes. New questions will be added by the ISARIC team and the wider scientific community, enabling the creation and sharing of new pipelines.

See [VERTEX](https://github.com/ISARICResearch/VERTEX) To download the code that can be used for ARC-structured data visualization.


[![Watch the video](https://i.sstatic.net/Vp2cE.png]
(https://github.com/ISARICResearch/.github/blob/main/profile/ISARIC_platform1_.mp4)


## Additional Services

### Data Management Services

ISARIC can provide guidance and files to launch your own data management system at your site. ISARIC also hosts a central REDCap data management system that can be used by sites around the world to enter or map data to standardized case record forms. Sites control the data they enter, and ISARIC supports user management and guidance.

### Analytic Support

ISARIC has a central data pipeline and analytic tools with dashboards, models, and descriptive statistic outputs. Contact us to see what we have that fits your needs.



---


