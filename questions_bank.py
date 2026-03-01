"""
Question Bank for Specialization Assessment
15-25 questions per specialization with skill mapping
"""

QUESTIONS_BANK = {
    "Machine Learning Engineer": [
        {
            "id": "ml_1",
            "question": "What is the main difference between supervised and unsupervised learning?",
            "options": ["Supervised uses labeled data, unsupervised doesn't", "Unsupervised is faster", "Supervised requires more data", "No difference"],
            "correct": 0,
            "skill": "ML Theory"
        },
        {
            "id": "ml_2",
            "question": "Which algorithm is best for handling missing values in a dataset?",
            "options": ["Mean imputation", "KNN imputation", "Drop missing rows", "All are equivalent"],
            "correct": 1,
            "skill": "Data Preprocessing"
        },
        {
            "id": "ml_3",
            "question": "What does cross-validation help prevent?",
            "options": ["Overfitting", "Underfitting", "Data leakage", "Both A and C"],
            "correct": 3,
            "skill": "Model Evaluation"
        },
        {
            "id": "ml_4",
            "question": "In Python, which library is primarily used for machine learning?",
            "options": ["NumPy", "Pandas", "Scikit-learn", "Matplotlib"],
            "correct": 2,
            "skill": "Python"
        },
        {
            "id": "ml_5",
            "question": "What is the purpose of feature scaling?",
            "options": ["To reduce dataset size", "To normalize feature ranges", "To remove outliers", "To encode categories"],
            "correct": 1,
            "skill": "Data Preprocessing"
        },
        {
            "id": "ml_6",
            "question": "Which metric is best for imbalanced classification?",
            "options": ["Accuracy", "F1-score", "Precision", "Recall"],
            "correct": 1,
            "skill": "Model Evaluation"
        },
        {
            "id": "ml_7",
            "question": "What is gradient descent used for?",
            "options": ["Data visualization", "Optimizing model parameters", "Feature selection", "Data cleaning"],
            "correct": 1,
            "skill": "ML Theory"
        },
        {
            "id": "ml_8",
            "question": "In a neural network, what does the activation function do?",
            "options": ["Adds bias", "Introduces non-linearity", "Normalizes inputs", "Reduces overfitting"],
            "correct": 1,
            "skill": "Deep Learning"
        },
        {
            "id": "ml_9",
            "question": "What is the difference between bagging and boosting?",
            "options": ["Bagging uses parallel models, boosting uses sequential", "No difference", "Boosting is faster", "Bagging is more accurate"],
            "correct": 0,
            "skill": "Ensemble Methods"
        },
        {
            "id": "ml_10",
            "question": "Which technique helps prevent overfitting?",
            "options": ["Adding more features", "Increasing model complexity", "Regularization", "Using more training data only"],
            "correct": 2,
            "skill": "Model Optimization"
        },
        {
            "id": "ml_11",
            "question": "What is the purpose of a confusion matrix?",
            "options": ["To visualize model performance", "To preprocess data", "To select features", "To tune hyperparameters"],
            "correct": 0,
            "skill": "Model Evaluation"
        },
        {
            "id": "ml_12",
            "question": "In pandas, how do you handle categorical variables?",
            "options": ["pd.categorize()", "pd.get_dummies()", "pd.encode()", "pd.convert()"],
            "correct": 1,
            "skill": "Python"
        },
        {
            "id": "ml_13",
            "question": "What is the bias-variance tradeoff?",
            "options": ["Balance between model complexity and generalization", "Choosing between algorithms", "Data splitting strategy", "Feature selection method"],
            "correct": 0,
            "skill": "ML Theory"
        },
        {
            "id": "ml_14",
            "question": "Which method is used for hyperparameter tuning?",
            "options": ["Grid Search", "Random Search", "Bayesian Optimization", "All of the above"],
            "correct": 3,
            "skill": "Model Optimization"
        },
        {
            "id": "ml_15",
            "question": "What does PCA stand for and what is its purpose?",
            "options": ["Principal Component Analysis - dimensionality reduction", "Principal Component Analysis - classification", "Partial Component Analysis - feature selection", "Primary Component Analysis - data cleaning"],
            "correct": 0,
            "skill": "Dimensionality Reduction"
        }
    ],
    
    "Data Scientist": [
        {
            "id": "ds_1",
            "question": "What is the main goal of exploratory data analysis (EDA)?",
            "options": ["To build models", "To understand data patterns and relationships", "To clean data", "To visualize data only"],
            "correct": 1,
            "skill": "Data Analysis"
        },
        {
            "id": "ds_2",
            "question": "Which statistical test is used for comparing means of two groups?",
            "options": ["Chi-square test", "T-test", "ANOVA", "Correlation test"],
            "correct": 1,
            "skill": "Statistics"
        },
        {
            "id": "ds_3",
            "question": "What is the difference between correlation and causation?",
            "options": ["No difference", "Correlation implies causation", "Causation requires correlation but not vice versa", "They are unrelated"],
            "correct": 2,
            "skill": "Statistics"
        },
        {
            "id": "ds_4",
            "question": "In Python, which library is best for statistical analysis?",
            "options": ["NumPy", "Pandas", "SciPy", "Scikit-learn"],
            "correct": 2,
            "skill": "Python"
        },
        {
            "id": "ds_5",
            "question": "What is a p-value in hypothesis testing?",
            "options": ["Probability of observing data given null hypothesis", "Probability of null hypothesis being true", "Effect size", "Confidence interval"],
            "correct": 0,
            "skill": "Statistics"
        },
        {
            "id": "ds_6",
            "question": "Which visualization is best for showing distributions?",
            "options": ["Bar chart", "Histogram", "Line chart", "Pie chart"],
            "correct": 1,
            "skill": "Data Visualization"
        },
        {
            "id": "ds_7",
            "question": "What is the purpose of A/B testing?",
            "options": ["To compare two versions", "To test algorithms", "To validate hypotheses", "All of the above"],
            "correct": 3,
            "skill": "Experimental Design"
        },
        {
            "id": "ds_8",
            "question": "In pandas, how do you group data and calculate statistics?",
            "options": ["df.group()", "df.groupby()", "df.aggregate()", "df.summarize()"],
            "correct": 1,
            "skill": "Python"
        },
        {
            "id": "ds_9",
            "question": "What is feature engineering?",
            "options": ["Creating new features from existing data", "Selecting features", "Removing features", "Scaling features"],
            "correct": 0,
            "skill": "Feature Engineering"
        },
        {
            "id": "ds_10",
            "question": "Which metric is used for regression problems?",
            "options": ["Accuracy", "F1-score", "RMSE", "Precision"],
            "correct": 2,
            "skill": "Model Evaluation"
        },
        {
            "id": "ds_11",
            "question": "What is the purpose of a box plot?",
            "options": ["Show distributions and outliers", "Compare categories", "Show trends over time", "Show correlations"],
            "correct": 0,
            "skill": "Data Visualization"
        },
        {
            "id": "ds_12",
            "question": "What does SQL stand for and what is it used for?",
            "options": ["Structured Query Language - database queries", "Simple Query Language - data analysis", "Statistical Query Language - statistics", "Sequential Query Language - data processing"],
            "correct": 0,
            "skill": "SQL"
        },
        {
            "id": "ds_13",
            "question": "What is the central limit theorem?",
            "options": ["Sample means approximate normal distribution", "Large samples are always better", "Population follows normal distribution", "Variance decreases with sample size"],
            "correct": 0,
            "skill": "Statistics"
        },
        {
            "id": "ds_14",
            "question": "Which Python library is best for data visualization?",
            "options": ["Matplotlib", "Seaborn", "Plotly", "All of the above"],
            "correct": 3,
            "skill": "Data Visualization"
        },
        {
            "id": "ds_15",
            "question": "What is the difference between population and sample?",
            "options": ["Population is larger", "Sample is subset of population", "No difference", "Population is theoretical, sample is real"],
            "correct": 1,
            "skill": "Statistics"
        }
    ],
    
    "Cybersecurity Analyst": [
        {
            "id": "cyber_1",
            "question": "What is the primary goal of a firewall?",
            "options": ["To prevent unauthorized access", "To encrypt data", "To store backups", "To monitor performance"],
            "correct": 0,
            "skill": "Network Security"
        },
        {
            "id": "cyber_2",
            "question": "What does SIEM stand for?",
            "options": ["Security Information and Event Management", "System Integration and Event Monitoring", "Secure Internet and Email Management", "Security Intelligence and Emergency Management"],
            "correct": 0,
            "skill": "Security Monitoring"
        },
        {
            "id": "cyber_3",
            "question": "What is a zero-day vulnerability?",
            "options": ["A vulnerability with no patch available", "A vulnerability that occurs at midnight", "A vulnerability in zero systems", "A vulnerability that was never exploited"],
            "correct": 0,
            "skill": "Vulnerability Management"
        },
        {
            "id": "cyber_4",
            "question": "What is the purpose of penetration testing?",
            "options": ["To find vulnerabilities in systems", "To attack systems", "To monitor networks", "To encrypt data"],
            "correct": 0,
            "skill": "Penetration Testing"
        },
        {
            "id": "cyber_5",
            "question": "What does IDS stand for?",
            "options": ["Intrusion Detection System", "Internet Defense System", "Internal Data Security", "Integrated Defense System"],
            "correct": 0,
            "skill": "Network Security"
        },
        {
            "id": "cyber_6",
            "question": "What is social engineering?",
            "options": ["Manipulating people to reveal information", "Engineering social networks", "Social media security", "Community-based security"],
            "correct": 0,
            "skill": "Security Awareness"
        },
        {
            "id": "cyber_7",
            "question": "What is the difference between authentication and authorization?",
            "options": ["Authentication verifies identity, authorization grants access", "No difference", "Authorization verifies identity", "Authentication grants access"],
            "correct": 0,
            "skill": "Access Control"
        },
        {
            "id": "cyber_8",
            "question": "What is encryption used for?",
            "options": ["To protect data confidentiality", "To speed up data transfer", "To compress data", "To backup data"],
            "correct": 0,
            "skill": "Cryptography"
        },
        {
            "id": "cyber_9",
            "question": "What is a DDoS attack?",
            "options": ["Distributed Denial of Service", "Data Destruction of Systems", "Direct Denial of Service", "Digital Defense of Systems"],
            "correct": 0,
            "skill": "Threat Analysis"
        },
        {
            "id": "cyber_10",
            "question": "What is the purpose of vulnerability scanning?",
            "options": ["To identify security weaknesses", "To remove vulnerabilities", "To encrypt systems", "To backup data"],
            "correct": 0,
            "skill": "Vulnerability Management"
        },
        {
            "id": "cyber_11",
            "question": "What does CIA stand for in cybersecurity?",
            "options": ["Confidentiality, Integrity, Availability", "Central Intelligence Agency", "Computer Information Assurance", "Cybersecurity Information Analysis"],
            "correct": 0,
            "skill": "Security Principles"
        },
        {
            "id": "cyber_12",
            "question": "What is a honeypot?",
            "options": ["A decoy system to attract attackers", "A secure storage system", "A backup system", "A monitoring tool"],
            "correct": 0,
            "skill": "Threat Detection"
        },
        {
            "id": "cyber_13",
            "question": "What is the difference between symmetric and asymmetric encryption?",
            "options": ["Symmetric uses one key, asymmetric uses two keys", "No difference", "Symmetric is faster", "Asymmetric is more secure"],
            "correct": 0,
            "skill": "Cryptography"
        },
        {
            "id": "cyber_14",
            "question": "What is incident response?",
            "options": ["Process for handling security breaches", "Preventing incidents", "Monitoring systems", "Backing up data"],
            "correct": 0,
            "skill": "Incident Response"
        },
        {
            "id": "cyber_15",
            "question": "What is the purpose of a security policy?",
            "options": ["To define security rules and procedures", "To encrypt data", "To monitor networks", "To backup systems"],
            "correct": 0,
            "skill": "Security Management"
        }
    ],
    
    "Full-Stack Developer": [
        {
            "id": "fs_1",
            "question": "What is the difference between frontend and backend?",
            "options": ["Frontend is user interface, backend is server logic", "No difference", "Backend is user interface", "Frontend is server logic"],
            "correct": 0,
            "skill": "Web Development"
        },
        {
            "id": "fs_2",
            "question": "What does REST stand for?",
            "options": ["Representational State Transfer", "Remote Execution State Transfer", "Resource Exchange State Transfer", "Reliable Execution State Transfer"],
            "correct": 0,
            "skill": "API Design"
        },
        {
            "id": "fs_3",
            "question": "What is the purpose of a database index?",
            "options": ["To speed up queries", "To store data", "To backup data", "To encrypt data"],
            "correct": 0,
            "skill": "Database"
        },
        {
            "id": "fs_4",
            "question": "What is the difference between SQL and NoSQL databases?",
            "options": ["SQL is relational, NoSQL is non-relational", "No difference", "SQL is faster", "NoSQL is more secure"],
            "correct": 0,
            "skill": "Database"
        },
        {
            "id": "fs_5",
            "question": "What is version control used for?",
            "options": ["To track code changes", "To compile code", "To deploy applications", "To test code"],
            "correct": 0,
            "skill": "Version Control"
        },
        {
            "id": "fs_6",
            "question": "What is the purpose of unit testing?",
            "options": ["To test individual components", "To test entire systems", "To deploy applications", "To document code"],
            "correct": 0,
            "skill": "Testing"
        },
        {
            "id": "fs_7",
            "question": "What is a microservice architecture?",
            "options": ["Small, independent services", "Large monolithic services", "Database architecture", "Network architecture"],
            "correct": 0,
            "skill": "Architecture"
        },
        {
            "id": "fs_8",
            "question": "What does HTTP stand for?",
            "options": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "Hyper Transfer Text Protocol", "High Text Transfer Protocol"],
            "correct": 0,
            "skill": "Web Protocols"
        },
        {
            "id": "fs_9",
            "question": "What is the purpose of Docker?",
            "options": ["Containerization", "Virtualization", "Cloud computing", "Database management"],
            "correct": 0,
            "skill": "DevOps"
        },
        {
            "id": "fs_10",
            "question": "What is the difference between GET and POST requests?",
            "options": ["GET retrieves data, POST sends data", "No difference", "POST retrieves data", "GET sends data"],
            "correct": 0,
            "skill": "API Design"
        },
        {
            "id": "fs_11",
            "question": "What is the purpose of middleware?",
            "options": ["To process requests between client and server", "To store data", "To render UI", "To compile code"],
            "correct": 0,
            "skill": "Backend Development"
        },
        {
            "id": "fs_12",
            "question": "What is the difference between synchronous and asynchronous code?",
            "options": ["Synchronous blocks, asynchronous doesn't", "No difference", "Asynchronous is slower", "Synchronous is always better"],
            "correct": 0,
            "skill": "Programming Concepts"
        },
        {
            "id": "fs_13",
            "question": "What is the purpose of environment variables?",
            "options": ["To store configuration", "To store data", "To encrypt data", "To backup data"],
            "correct": 0,
            "skill": "Configuration Management"
        },
        {
            "id": "fs_14",
            "question": "What is the difference between stateful and stateless applications?",
            "options": ["Stateful remembers state, stateless doesn't", "No difference", "Stateless remembers state", "Stateful is always better"],
            "correct": 0,
            "skill": "Architecture"
        },
        {
            "id": "fs_15",
            "question": "What is the purpose of CI/CD?",
            "options": ["Continuous Integration and Deployment", "Code Integration", "Data Integration", "System Integration"],
            "correct": 0,
            "skill": "DevOps"
        }
    ]
}

# Add questions for remaining specializations (simplified for space)
# In production, each specialization would have 15-25 unique questions

def get_questions_for_specialization(specialization, num_questions=15):
    """Get questions for a specific specialization"""
    if specialization in QUESTIONS_BANK:
        questions = QUESTIONS_BANK[specialization]
        return questions[:num_questions] if len(questions) >= num_questions else questions
    else:
        # Return generic questions if specialization not found
        return QUESTIONS_BANK["Full-Stack Developer"][:num_questions]

def get_all_specializations():
    """Get list of all specializations"""
    return list(QUESTIONS_BANK.keys())

