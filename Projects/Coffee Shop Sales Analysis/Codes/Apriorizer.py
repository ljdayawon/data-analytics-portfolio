# This script reads transaction data, applies the Apriori algorithm to find 
# frequent itemsets, generates association rules with lift and conviction metrics, 
# formats the rules for readability and Tableau visualization, and exports the results to an Excel file.

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

#Load transaction data
input_path = r"C:\Users\ADMIN\Desktop\IPT Final Project\ReadyForApriori.xlsx"
df = pd.read_excel(input_path)

#Drop transaction ID column for analysis
basket = df.drop('transaction_id', axis=1)

#Convert to boolean to comply with mlxtend
basket = basket.astype(bool)

#Generate frequent itemsets
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)

#Generate association rules (min lift = 1.0)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

#Fix conviction and handle infinite values
rules['conviction'] = (1 - rules['consequent support']) / (1 - rules['confidence'])

#Avoid chained assignment warning
rules['conviction'] = rules['conviction'].replace([float('inf'), -float('inf')], None)

#Format sets into readable strings
rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
rules['rule'] = rules['antecedents'] + ' → ' + rules['consequents']

#Abbreviate for Tableau (unique initials)
abbrev_map = {
    'Bakery': 'Bk',
    'Branded': 'Br',
    'Coffee': 'C',
    'Coffee Beans': 'CB',
    'Drinking Chocolate': 'DC',
    'Flavours': 'F',
    'Loose Tea': 'LT',
    'Packaged Chocolate': 'PC',
    'Tea': 'T'
}

def abbreviate_items(item_string):
    items = item_string.split(', ')
    return ', '.join(abbrev_map.get(item.strip(), item.strip()) for item in items)

#Abbreviate antecedents and consequents separately
rules['antecedents_initials'] = rules['antecedents'].apply(abbreviate_items)
rules['consequents_initials'] = rules['consequents'].apply(abbreviate_items)

#Create rule string using initials (for Tableau)
rules['rule_initials'] = rules['antecedents_initials'] + ' → ' + rules['consequents_initials']

#Round values for Tableau
rules[['support', 'confidence', 'lift', 'conviction']] = rules[['support', 'confidence', 'lift', 'conviction']].round(4)

#Final columns for export
final_cols = [
    'rule', 'rule_initials',
    'antecedents', 'antecedents_initials',
    'consequents', 'consequents_initials',
    'support', 'confidence', 'lift', 'conviction'
]
rules = rules[final_cols]

#Save to Excel
output_path = r"C:\Users\ADMIN\Desktop\IPT Final Project\AssociationRules.xlsx"
rules.to_excel(output_path, index=False)

print(f"Association rules saved to: {output_path}")
