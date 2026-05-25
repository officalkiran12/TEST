import sqlite3
conn = sqlite3.connect('jobs.db')
cur = conn.cursor()

# Non-http links
cur.execute("SELECT id, title, apply_link, source FROM jobs WHERE apply_link NOT LIKE 'http%' LIMIT 20")
print('=== NON-HTTP APPLY_LINKS ===')
for r in cur.fetchall():
    print('ID={:5} | {:50s} | LINK={:100s} | SRC={}'.format(r[0], str(r[1])[:50], str(r[2])[:100], r[3]))
print()

# Sources distribution
cur.execute('SELECT source, COUNT(*) FROM jobs GROUP BY source ORDER BY COUNT(*) DESC')
print('=== JOBS BY SOURCE ===')
for r in cur.fetchall():
    print('  {:30s}: {}'.format(str(r[0]), r[1]))
print()

# Linkedin URLs
cur.execute("SELECT id, title, apply_link, source FROM jobs WHERE apply_link LIKE '%linkedin.com%' LIMIT 10")
print('=== LINKEDIN URLS ===')
for r in cur.fetchall():
    print('ID={:5} | {:50s} | {}'.format(r[0], str(r[1])[:50], str(r[2])[:100]))
print()

# Unique sources
cur.execute('SELECT DISTINCT source FROM jobs ORDER BY source')
print('=== UNIQUE SOURCES ===')
for r in cur.fetchall():
    print('  - {}'.format(str(r[0])))
print()

# Count refId patterns
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE '%refId=%'")
print('URLs with refId param: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE '%ref=%'")
print('URLs with ref param: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE '%psc.gov.np%'")
print('URLs pointing to psc.gov.np: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE '%merojob.com%'")
print('URLs pointing to merojob.com: {}'.format(cur.fetchone()[0]))

# Check URL validity
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://www.linkedin.com/jobs/search%'")
print('LinkedIn search (not job-specific) URLs: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://www.upwork.com/search/jobs/%'")
print('Upwork search (not job-specific) URLs: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://weworkremotely.com/remote-jobs/search%'")
print('WWR search (not job-specific) URLs: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://merojob.com/search/%'")
print('Merojob search (not job-specific) URLs: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://psc.gov.np/vacancy%'")
print('PSC vacancy (not job-specific) URLs: {}'.format(cur.fetchone()[0]))

# Check if any links are real job-specific links
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://remoteok.com/remote-jobs/%'")
print('RemoteOK job-specific URLs: {}'.format(cur.fetchone()[0]))
cur.execute("SELECT COUNT(*) FROM jobs WHERE apply_link LIKE 'https://www.linkedin.com/jobs/view%'")
print('LinkedIn job-specific URLs: {}'.format(cur.fetchone()[0]))

conn.close()
