import random
from datetime import datetime, timedelta
from .models import Article, User

def seed_db(db):
    # Clear everything first
    db.session.query(Article).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create users
    users = []
    for uname in ("alice", "bob", "charlie"):
        u = User(email=f"{uname}@example.com")

        # TODO: see task 2
        # u.password = "password"

        users.append(u)
        db.session.add(u)

    db.session.flush()  # assign IDs to users

    print( "Finding user Bob:", User.get_by_email("bob@example.com") )

    # Some sample cyber-security themed articles (you can replace with real ones)
    sample_articles = [
        {
            "title": "Ransomware attacks surge in 2025",
            "body": "New data shows ransomware attacks have increased sharply across multiple sectors in 2025.",
            "url": "https://example.com/ransomware-2025"
        },
        {
            "title": "Zero-day exploit discovered in major software",
            "body": "A new zero-day has been discovered targeting widely used productivity software.",
            "url": "https://example.com/zero-day-discovery"
        },
        {
            "title": "Supply chain attacks on open source packages",
            "body": "Attackers compromised dependencies in popular open source libraries to inject backdoors.",
            "url": "https://example.com/supply-chain-attack"
        },
        {
            "title": "AI-powered phishing campaigns spike",
            "body": "Phishing campaigns using AI to generate convincing emails have grown in number and sophistication.",
            "url": "https://example.com/ai-phishing"
        },
        {
            "title": "Security in IoT: vulnerabilities in smart home devices",
            "body": "Many smart home devices ship with weak default credentials and are easily compromised.",
            "url": "https://example.com/iot-vulnerabilities"
        },
        {
            "title": "Cloud misconfiguration causes data breach",
            "body": "A major cloud provider misconfiguration exposed millions of customer records.",
            "url": "https://example.com/cloud-misconfig"
        },
        {
            "title": "Critical flaw found in encryption library",
            "body": "A bug in a popular encryption library could allow decryption of communications.",
            "url": "https://example.com/encryption-flaw"
        },
        {
            "title": "APT group targets critical infrastructure",
            "body": "An advanced persistent threat group has been observed targeting power grids and utilities.",
            "url": "https://example.com/apt-infrastructure"
        },
        {
            "title": "Data theft through insider attacks increases",
            "body": "Insider threats contributed to many of the biggest breaches this year.",
            "url": "https://example.com/insider-threats"
        },
        {
            "title": "Emergence of quantum computing threats on cryptography",
            "body": "Researchers warn that quantum attacks may soon threaten classical cryptographic systems.",
            "url": "https://example.com/quantum-threat"
        },
        {
            "title": "Biometric spoofing attacks succeed in lab tests",
            "body": "A recent experiment shows fingerprint and face recognition systems can be fooled.",
            "url": "https://example.com/biometric-spoofing"
        },
        {
            "title": "Regulation tightening on data privacy and security",
            "body": "New laws in several countries aim to impose harsher penalties for data breaches.",
            "url": "https://example.com/privacy-regulation"
        },
    ]

    # Create 12 articles
    articles = []
    for art in sample_articles:
        # randomize created date within past 6 months
        days_ago = random.randint(0, 180)
        created_dt = datetime.utcnow() - timedelta(days=days_ago)
        a = Article(
            title=art["title"],
            body=art["body"],
            url=art["url"],
            created=created_dt
        )
        # assign a random user
        chosen_user = random.choice(users)
        a.user = chosen_user
        articles.append(a)
        db.session.add(a)

    # commit all
    db.session.commit()

    print(f"Seeded {len(users)} users and {len(articles)} articles.")
    article = Article.query.get(1)
    print("Article 1:", article, "Added by user:", article.user)
