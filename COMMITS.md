# Suggested Git Commit Messages

A professional, logically-ordered set of 25 commits for building this project.
Use them in sequence as you build (or to reconstruct a clean history).

```bash
git init
git add .gitignore README.md requirements.txt
git commit -m "chore: initialize project structure and add requirements"
```

1. `chore: initialize project structure and add requirements`
2. `docs: add project README with overview and run instructions`
3. `data: add loan prediction dataset and data folder`
4. `feat(eda): add data cleaning and missing-value handling`
5. `feat(eda): add outlier detection with boxplots`
6. `feat(eda): add feature engineering (total income, log loan, ratio)`
7. `feat(eda): add correlation heatmap and statistical insights`
8. `feat(eda): add histograms, bar charts and pairplot visualizations`
9. `feat(ml): add train/test split and feature scaling pipeline`
10. `feat(ml): implement Logistic Regression model`
11. `feat(ml): implement Decision Tree classifier`
12. `feat(ml): implement Random Forest classifier`
13. `feat(ml): add evaluation metrics (accuracy, precision, recall, F1)`
14. `feat(ml): add confusion matrices and ROC curve plots`
15. `feat(ml): save trained models as pickle files`
16. `feat(sim): scaffold SimPy bank queue M/M/c simulation`
17. `feat(sim): add random arrivals and multi-teller service logic`
18. `feat(sim): compute waiting time and teller utilization`
19. `feat(sim): generate queue-length, waiting-time and utilization graphs`
20. `feat(dashboard): scaffold Streamlit app with multi-page navigation`
21. `feat(dashboard): add overview and dataset analysis pages`
22. `feat(dashboard): add loan prediction page with live inference`
23. `feat(dashboard): add interactive simulation dashboard page`
24. `docs: add final project report and 12-slide presentation`
25. `docs: add viva Q&A, commit guide and finalize documentation`

## .gitignore (recommended)

```
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.DS_Store
node_modules/
```
