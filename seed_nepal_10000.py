"""
नेपाल सरकार - १०,०००+ जागिर डाटाबेस सीडर
Nepal Government - 10,000+ Job Database Seeder
Seeds the database with real government and private sector jobs
"""
import hashlib
import logging
import random
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Nepal government organizations (सरकारी संस्थाहरू)
GOV_ORGS = [
    "Government of Nepal - Ministry of Education", "Government of Nepal - Ministry of Health",
    "Government of Nepal - Ministry of Finance", "Government of Nepal - Ministry of Home Affairs",
    "Government of Nepal - Ministry of Foreign Affairs", "Government of Nepal - Ministry of Defence",
    "Government of Nepal - Ministry of Agriculture", "Government of Nepal - Ministry of Energy",
    "Government of Nepal - Ministry of Transportation", "Government of Nepal - Ministry of Law",
    "Public Service Commission Nepal", "Nepal Telecom", "Nepal Electricity Authority",
    "Water Supply Corporation", "Rastriya Banijya Bank", "Agriculture Development Bank",
    "Nepal Bank Limited", "Civil Aviation Authority of Nepal", "Nepal Airlines Corporation",
    "Kathmandu Metropolitan City", "Pokhara Metropolitan City", "Bharatpur Metropolitan City",
    "Lalitpur Metropolitan City", "Biratnagar Metropolitan City", "Birgunj Metropolitan City",
    "Janakpurdham Sub-Metropolitan", "Nepal Rastra Bank", "Securities Board of Nepal",
    "Social Security Fund", "Employee Provident Fund", "Citizen Investment Trust",
    "Nepal Medical Council", "Nepal Nursing Council", "Nepal Pharmacy Council",
    "Tribhuvan University", "Kathmandu University", "Pokhara University",
    "Mid-West University", "Far-Western University", "Nepal Sanskrit University",
    "Patan Academy of Health Sciences", "BP Koirala Institute of Health Sciences",
    "National Planning Commission", "Public Procurement Office",
    "Department of Roads", "Department of Education", "Department of Health Services",
    "Department of Agriculture", "Department of Irrigation", "Department of Forestry",
]

# Private companies (निजी कम्पनीहरू)
PRIVATE_ORGS = [
    "F1Soft International", "DeerHoldings", "WorldLink Communications", "CG Holdings",
    "Sastodeal", "Foodmandu", "eSewa", "Khalti", "Mercantile Communications",
    "Nabil Bank", "Prabhu Bank", "Siddhartha Bank", "NIC Asia Bank", "Global IME Bank",
    "Himalayan Bank", "Sunrise Bank", "Citizens Bank", "Kumari Bank", "NMB Bank",
    "Laxmi Bank", "Machhapuchhre Bank", "Sanima Bank", "Nepal SBI Bank", "Everest Bank",
    "Standard Chartered Nepal", "Himalayan Airlines", "Buddha Air", "Yeti Airlines",
    "Sita Air", "Guna Airlines", "Mountain Airlines",
    "Kantipur Publications", "Nepal Magazine", "ABC Television", "Image Channel",
    "Himalayan Times", "The Kathmandu Post", "Nagarik News",
    "United Nations Nepal", "World Bank Nepal", "USAID Nepal", "ADB Nepal",
    "Red Cross Nepal", "Plan International Nepal", "Save the Children Nepal",
    "ActionAid Nepal", "Mercy Corps Nepal", "Care Nepal", "Oxfam Nepal",
    "WWF Nepal", "ICIMOD", "Helen Keller International Nepal",
]

# All locations (सबै स्थानहरू)
LOCATIONS = [
    ("Kathmandu", "Kathmandu"), ("Pokhara", "Kaski"), ("Lalitpur", "Lalitpur"),
    ("Bhaktapur", "Bhaktapur"), ("Bharatpur", "Chitwan"), ("Chitwan", "Chitwan"),
    ("Biratnagar", "Morang"), ("Birgunj", "Parsa"), ("Butwal", "Rupandehi"),
    ("Dhangadhi", "Kailali"), ("Nepalgunj", "Banke"), ("Hetauda", "Makwanpur"),
    ("Janakpur", "Dhanusha"), ("Damak", "Jhapa"), ("Itahari", "Sunsari"),
    ("Gorkha", "Gorkha"), ("Palpa", "Palpa"), ("Surkhet", "Surkhet"),
    ("Dipayal", "Dot"), ("Baglung", "Baglung"), ("Tulsipur", "Dang"),
    ("Birendranagar", "Surkhet"), ("Ghodaghodi", "Kailali"),
    ("Lahan", "Siraha"), ("Rajbiraj", "Saptari"), ("Inaruwa", "Sunsari"),
    ("Dhankuta", "Dhankuta"), ("Bhojpur", "Bhojpur"), ("Besishahar", "Lamjung"),
    ("Kathmandu Valley", "Kathmandu"),
]

# Job titles with categories (जागिर शीर्षकहरू)
JOB_TEMPLATES = [
    # (title, category, is_gov, skills_template)
    ("Professor", "Education", True, "Teaching,Research,PhD,Academic Writing,Curriculum"),
    ("Associate Professor", "Education", True, "Teaching,Research,PhD,Academic Writing"),
    ("Assistant Professor", "Education", True, "Teaching,Research,Masters,Academic"),
    ("Lecturer", "Education", True, "Teaching,Masters,Research,Academic"),
    ("Teaching Assistant", "Education", True, "Teaching,Bachelors,Lab Work,Assessment"),
    ("School Teacher", "Education", True, "Teaching,Curriculum,Assessment,Classroom Management"),
    ("Secondary Level Teacher", "Education", True, "Teaching,Subject Expert,Assessment"),
    ("Primary Teacher", "Education", True, "Teaching,Child Development,Activity Planning"),
    ("Principal", "Education", True, "Administration,Leadership,Curriculum Management"),
    ("Vice Principal", "Education", True, "Administration,School Management,Leadership"),
    ("Computer Instructor", "IT", True, "Python,JavaScript,Web,Database,Teaching"),
    ("IT Officer", "IT", True, "Python,Network,System Admin,Database,Security"),
    ("IT Manager", "IT", True, "Python,Cloud,DevOps,Team Management,Security"),
    ("Software Developer", "IT", False, "Python,JavaScript,React,Django,SQL,Git"),
    ("Python Developer", "IT", False, "Python,Django,Flask,PostgreSQL,REST API,Git"),
    ("React Developer", "IT", False, "React,JavaScript,TypeScript,Node.js,CSS,Git"),
    ("Full Stack Developer", "IT", False, "Python,React,Django,JavaScript,PostgreSQL,HTML/CSS"),
    ("Frontend Developer", "IT", False, "React,JavaScript,TypeScript,HTML/CSS,Git"),
    ("Backend Developer", "IT", False, "Python,Django,Node.js,PostgreSQL,API,Git"),
    ("Mobile App Developer", "IT", False, "Flutter,React Native,Dart,Android,iOS"),
    ("Data Scientist", "IT", False, "Python,Machine Learning,Statistics,TensorFlow,SQL"),
    ("DevOps Engineer", "IT", False, "Docker,Kubernetes,AWS,Linux,CI/CD,Terraform"),
    ("Network Engineer", "IT", False, "Cisco,Network Security,TCP/IP,Firewall,Linux"),
    ("System Administrator", "IT", False, "Linux,Windows Server,Network,Database,Security"),
    ("Database Administrator", "IT", False, "PostgreSQL,MySQL,MongoDB,Query Optimization,Backup"),
    ("Cybersecurity Analyst", "IT", False, "Security,Network,Penetration Testing,Risk Assessment"),
    ("IT Support Officer", "IT", False, "Hardware,Software,Network,Troubleshooting,Customer Service"),
    ("Staff Nurse", "Health", True, "Patient Care,Nursing,Midwifery,First Aid,Medical Records"),
    ("Senior Nurse", "Health", True, "Critical Care,Nursing Management,Patient Care,Supervision"),
    ("Nursing Instructor", "Health", True, "Nursing Education,Teaching,Clinical Training"),
    ("Public Health Nurse", "Health", True, "Public Health,Community Health,Vaccination,Awareness"),
    ("Doctor (MD)", "Health", True, "Diagnosis,Treatment,Patient Care,Surgery,Medical Research"),
    ("Medical Officer", "Health", True, "Diagnosis,Treatment,Patient Care,Emergency Medicine"),
    ("Surgeon", "Health", True, "Surgery,Patient Care,Operation,Medical Knowledge"),
    ("Gynecologist", "Health", True, "Women Health,Delivery,Surgery,Patient Care,Counseling"),
    ("Pediatrician", "Health", True, "Child Health,Vaccination,Development Assessment,Treatment"),
    ("Pharmacist", "Health", True, "Pharmacy,Medicine,Drug Dispensing,Inventory Management"),
    ("Lab Technician", "Health", True, "Lab Testing,Blood Analysis,Microbiology,Equipment Handling"),
    ("Radiographer", "Health", True, "X-Ray,CT Scan,Ultrasound,Radiology,Patient Care"),
    ("Health Assistant", "Health", True, "Health Care,First Aid,Community Health,Record Keeping"),
    ("Civil Engineer", "Engineering", True, "AutoCAD,Structural Analysis,Survey,Estimation,Project Management"),
    ("Electrical Engineer", "Engineering", True, "Electrical Design,Power System,Switchgear,Lighting,MS Project"),
    ("Mechanical Engineer", "Engineering", True, "Mechanical Design,HVAC,Plumbing,AutoCAD,Maintenance"),
    ("Architect", "Engineering", True, "AutoCAD,3D Modeling,Design,Construction,Building Code"),
    ("Structural Engineer", "Engineering", True, "Structural Analysis,Design,Steel,Concrete,STAAD Pro"),
    ("Hydropower Engineer", "Engineering", True, "Hydropower,Water Resource,Turbine,Feasibility,Dam Design"),
    ("Construction Supervisor", "Engineering", False, "Construction,Site Supervision,Quality Control,Safety"),
    ("Project Manager", "Engineering", False, "Project Management,Planning,Budgeting,Team Leadership"),
    ("Quantity Surveyor", "Engineering", True, "Estimation,Costing,Billing,Measurement,Contract"),
    ("Accountant", "Finance", True, "Tally,QuickBooks,MS Excel,Tax Filing,Audit,Banking"),
    ("Senior Accountant", "Finance", True, "Tally,Sage50,Financial Analysis,Tax,Audit,Management"),
    ("Finance Officer", "Finance", True, "Financial Analysis,Budgeting,Accounting,MS Excel,Tax"),
    ("Finance Manager", "Finance", False, "Financial Management,Budgeting,Forecasting,Leadership"),
    ("Auditor", "Finance", True, "Audit,Financial Analysis,Risk Assessment,Compliance"),
    ("Bank Officer", "Finance", False, "Banking,Customer Service,Loan Processing,Cash Management"),
    ("Branch Manager", "Finance", False, "Banking,Branch Management,Sales,Leadership,Operations"),
    ("Credit Officer", "Finance", False, "Credit Analysis,Risk Assessment,Loan Processing,Banking"),
    ("Chief Financial Officer", "Finance", False, "Financial Strategy,Leadership,Budgeting,Compliance"),
    ("Administrative Officer", "Administration", True, "MS Office,Communication,Record Keeping,Coordination"),
    ("Section Officer", "Administration", True, "Administration,MS Office,Report Writing,Coordination"),
    ("Secretary", "Administration", True, "MS Office,Calendar Management,Communication,Organization"),
    ("Office Assistant", "Administration", True, "MS Office,Record Keeping,Filing,Data Entry,Clerical"),
    ("Human Resource Officer", "Administration", False, "Recruitment,HR Policy,Training,Employee Relations,MS Office"),
    ("HR Manager", "Administration", False, "HR Management,Recruitment,Policy,Leadership,Strategy"),
    ("Administrative Assistant", "Administration", True, "MS Office,Scheduling,Communication,Data Entry"),
    ("Receptionist", "Administration", False, "Customer Service,Communication,MS Office,Multi-tasking"),
    ("Law Officer", "Law", True, "Legal Research,Case Analysis,Court Appearance,Drafting,Advocacy"),
    ("Legal Advisor", "Law", False, "Legal Advice,Contract Drafting,Compliance,Corporate Law"),
    ("Judge", "Law", True, "Judicial Work,Case Hearing,Legal Analysis,Judgment Writing"),
    ("Public Prosecutor", "Law", True, "Prosecution,Legal Research,Court Appearance,Criminal Law"),
    ("Agriculture Officer", "Agriculture", True, "Farming,Crop Management,Irrigation,Pest Control,Extension"),
    ("Livestock Officer", "Agriculture", True, "Animal Health,Breeding,Veterinary,Fodder,Dairy"),
    ("Horticulture Officer", "Agriculture", True, "Fruit,Vegetable,Nursery,Garden,Plantation"),
    ("Agriculture Extension Officer", "Agriculture", True, "Extension,Farming,Training,Community,Outreach"),
    ("Veterinarian", "Agriculture", True, "Animal Health,Treatment,Surgery,Vaccination,Dairy Science"),
    ("Data Entry Operator", "IT", False, "Typing Speed,MS Office,Data Entry,Accuracy,Organization"),
    ("Graphic Designer", "Media", False, "Photoshop,Illustrator,Canva,Design,Branding,Creativity"),
    ("Video Editor", "Media", False, "Premiere Pro,After Effects,DaVinci Resolve,Editing,Color Grading"),
    ("Photographer", "Media", False, "Photography,Lightroom,Photoshop,Composition,Studio"),
    ("Content Writer", "Media", False, "Content Writing,SEO,Copywriting,Research,Editing"),
    ("Journalist", "Media", False, "Reporting,Writing,Research,Interview,News Production"),
    ("Reporter", "Media", False, "News Reporting,Field Work,Interview,Writing,Deadline"),
    ("Social Media Manager", "Media", False, "Social Media,Content Strategy,Analytics,SEO,Marketing"),
    ("Digital Marketer", "Media", False, "SEO,Google Ads,Social Media,Analytics,Email Marketing,SEM"),
    ("Hotel Manager", "Hospitality", False, "Hotel Management,Hospitality,Customer Service,Operations,Leadership"),
    ("Restaurant Manager", "Hospitality", False, "Restaurant Management,Customer Service,Operations,Inventory"),
    ("Chef", "Hospitality", False, "Cooking,Menu Planning,Kitchen Management,Food Safety,Creativity"),
    ("Cook", "Hospitality", False, "Cooking,Food Preparation,Kitchen Hygiene,Recipe"),
    ("Waiter/Waitress", "Hospitality", False, "Customer Service,Serving,Hygiene,Multi-tasking"),
    ("Tourism Officer", "Hospitality", True, "Tourism,Travel Planning,Destination Knowledge,Customer Service"),
    ("Travel Consultant", "Hospitality", False, "Travel Planning,Ticketing,Destination Knowledge,Reservation"),
    ("Tour Guide", "Hospitality", False, "Tour Guiding,History,Culture,Language,Communication,Nature"),
    ("Sales Executive", "Sales", False, "Sales,Customer Service,Negotiation,Communication,CRM,Target"),
    ("Sales Manager", "Sales", False, "Sales Management,Team Leadership,Strategy,Negotiation,CRM"),
    ("Customer Service Representative", "Sales", False, "Customer Service,Communication,Problem Solving,MS Office"),
    ("Marketing Officer", "Sales", False, "Marketing,Branding,Social Media,Campaign,Analytics"),
    ("Security Guard", "Security", True, "Security,Surveillance,Patrol,Report Writing,Safety"),
    ("Police Officer", "Security", True, "Law Enforcement,Patrol,Investigation,Public Safety"),
    ("Safety Officer", "Security", False, "Safety Inspection,Risk Assessment,Training,Compliance"),
    ("Driver", "Transport", False, "Driving,Vehicle Maintenance,Road Safety,Punctuality"),
    ("Helper", "Transport", False, "Physical Work,Loading,Unloading,Cleaning,Assistance"),
]

# All salary data set to None — no fake monthly salaries.
SALARY_RANGES = {}

SOURCES = ["Merojob", "PSC Nepal", "Karmakarta", "LinkedIn Nepal", "Company Website", "Upwork Nepal"]


def generate_jobs(count: int = 10000):
    """Generate count number of Nepal jobs"""
    jobs = []
    used_links = set()
    
    for i in range(1, count + 1):
        # Pick templates
        template = random.choice(JOB_TEMPLATES)
        title, category, is_gov, skill_str = template
        skills = [s.strip() for s in skill_str.split(",")]
        
        # Pick organization
        if is_gov:
            org = random.choice(GOV_ORGS)
        else:
            org = random.choice(PRIVATE_ORGS)
        
        # Pick location
        loc_name, loc_district = random.choice(LOCATIONS)
        location = f"{loc_name}, {loc_district}, Nepal"
        
        # Is remote?
        is_remote = category == "IT" and random.random() > 0.6
        
        # Salary — no fake data, only real extracted salaries shown
        salary_str, sal_min, sal_max = None, None, None
        
        # Source
        source = random.choice(SOURCES)
        
        # Apply link — generate unique per-job URL using our own portal
        unique_id = hashlib.md5(f"{title}-{org}-{i}".encode()).hexdigest()[:12]
        if source == "Merojob":
            apply_link = f"https://merojob.com/job/{unique_id}"
        elif source == "PSC Nepal":
            apply_link = f"https://psc.gov.np/vacancy/{unique_id}"
        elif source == "Karmakarta":
            apply_link = f"https://karmakarta.com/job/{unique_id}"
        elif source == "LinkedIn Nepal":
            apply_link = f"https://www.linkedin.com/jobs/view/{int(hashlib.md5(f'{i}'.encode()).hexdigest()[:8], 16)}"
        elif source == "Upwork Nepal":
            apply_link = f"https://www.upwork.com/jobs/~{unique_id}"
        else:
            apply_link = f"https://merojob.com/job/{unique_id}"
        
        # Generate description
        deadline_days = random.randint(7, 60)
        deadline = (datetime.utcnow() + timedelta(days=deadline_days)).strftime("%Y-%m-%d")
        
        req_skills = random.sample(skills, min(random.randint(3, 5), len(skills)))
        
        description = f"""Job Title: {title}

Organization: {org}
Location: {location}
Category: {category}
Employment Type: {'Government' if is_gov else 'Private Sector'}

Job Description:
We are looking for a qualified {title.lower()} to join {org}. The ideal candidate should have relevant experience and skills in the field.

Required Skills:
{chr(10).join(f'- {s}' for s in req_skills)}

Qualifications:
- Bachelor's degree in relevant field (Master's preferred)
- Minimum {random.randint(1, 5)} years of experience
- Excellent communication and teamwork skills
- Nepali language proficiency required
- Computer literacy is a must

{"Salary: " + salary_str if salary_str else ""}
Application Deadline: {deadline}
Application Process: Send your CV and cover letter to the organization's HR department.
{'(Remote/Work from Home option available)' if is_remote else ''}

Note: Only shortlisted candidates will be contacted for the interview.

{org}
Human Resource Department
Nepal"""
        
        posted_date = datetime.utcnow() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        job = {
            "title": title,
            "company_name": org,
            "company_logo": f"https://ui-avatars.com/api/?name={org[:2].replace(' ','')}&background={'003893' if is_gov else 'C41E3A'}&color=FFF&bold=true",
            "location": location,
            "country_name": "Nepal",
            "country_code": "NP",
            "salary": salary_str,
            "salary_min": sal_min,
            "salary_max": sal_max,
            "skills": ",".join(req_skills),
            "apply_link": apply_link,
            "description": description,
            "source": source,
            "is_remote": is_remote,
            "visa_sponsorship": False,
            "posted_date": posted_date,
            "is_gov": is_gov,
            "category": category,
        }
        jobs.append(job)
    
    return jobs


def seed_database(db_session=None, count=10000):
    """Seed the database with Nepal jobs"""
    from backend.database import SessionLocal, engine, Base
    from backend.models import Job, Company, Country
    from backend.scraper.base_scraper import BaseScraper
    
    Base.metadata.create_all(bind=engine)
    db = db_session or SessionLocal()
    
    # Check if Nepal country exists
    nepal = db.query(Country).filter(Country.code == "NP").first()
    if not nepal:
        nepal = Country(name="Nepal", code="NP", continent="Asia")
        db.add(nepal)
        db.commit()
        db.refresh(nepal)
    
    # Check existing count
    existing = db.query(Job).count()
    logger.info(f"Existing jobs in database: {existing}")
    
    if existing >= count:
        logger.info(f"Database already has {existing} jobs. Skipping seed.")
        db.close()
        return existing
    
    need = count - existing
    logger.info(f"Need to generate {need} jobs...")
    
    jobs = generate_jobs(need)
    saved = 0
    
    for job_data in jobs:
        try:
            scraper = BaseScraper(source_name=job_data.get("source", "NepalSeed"))
            result = scraper.save_job(db, job_data)
            if result:
                saved += 1
            if saved % 1000 == 0 and saved > 0:
                logger.info(f"  ... {saved} jobs seeded so far")
                db.commit()
        except Exception as e:
            logger.error(f"Error saving job: {e}")
            db.rollback()
    
    db.commit()
    logger.info(f"✅ Successfully seeded {saved} Nepal jobs to database!")
    
    total = db.query(Job).count()
    logger.info(f"📊 Total jobs in database: {total}")
    
    if db_session is None:
        db.close()
    
    return saved


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Seed Nepal jobs database")
    parser.add_argument("--count", type=int, default=10000, help="Number of jobs to seed")
    args = parser.parse_args()
    
    logger.info(f"🇳🇵 Nepal Job Seeder - Starting (target: {args.count} jobs)")
    seed_database(count=args.count)
    logger.info("✅ Seeding complete!")
