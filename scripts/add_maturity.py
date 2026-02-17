import json
import datetime

# Approximate creation dates (year only for simplicity)
creation_dates = {
    'Python': 1991,
    'Java': 1995,
    'Django': 2005,
    'Flask': 2010,
    'Express': 2010,
    'Spring Boot': 2014,
    'Rails': 2004,
    'PostgreSQL': 1996,
    'MySQL': 1995,
    'MongoDB': 2009,
    'Redis': 2009,
    'Elasticsearch': 2010,
    'RabbitMQ': 2007,
    'Apache Kafka': 2011,
    'Keycloak': 2014,
    'Ory Kratos': 2019,
    'Prometheus': 2012,
    'Grafana': 2014,
    'Jaeger': 2016,
    'Terraform': 2014,
    'Ansible': 2012,
    'Node.js': 2009,
    'Deno': 2018,
    'Logstash': 2009,
}

current_year = datetime.datetime.now().year

def calculate_maturity(creation_year):
    """Calculate maturity score based on project age"""
    age = current_year - creation_year
    
    if age >= 20:
        return 1.0  # Battle-tested, decades old
    elif age >= 15:
        return 0.95
    elif age >= 10:
        return 0.9
    elif age >= 8:
        return 0.85
    elif age >= 5:
        return 0.8
    elif age >= 3:
        return 0.7
    elif age >= 1:
        return 0.6
    else:
        return 0.5  # New projects

# Load the data
with open('data/projects_architectural.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('='*50)
print('CALCULATING MATURITY SCORES')
print('='*50)

for name, proj in data.items():
    if name in creation_dates:
        year = creation_dates[name]
        age = current_year - year
        maturity = calculate_maturity(year)
        proj['maturity_score'] = maturity
        print(f'✅ {name}: Created {year} ({age} years) → Maturity: {maturity:.2f}')
    else:
        print(f'⚠️  {name}: No creation date, using default 0.7')
        proj['maturity_score'] = 0.7

# Save updated data
with open('data/projects_architectural.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('\n✅ Updated maturity scores saved')
