from collections import Counter


external = {}
with open("resources/HSDB.txt", encoding='utf-8') as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("resources/DrugBank.txt", encoding='utf-8') as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

drug_suffix_counter = Counter()
brand_suffix_counter = Counter()

for name, category in external.items():
    suffix = name[-7:]  # Get the last 7 characters as suffix
    if category == 'drug':
        drug_suffix_counter[suffix] += 1
    elif category == 'brand':
        brand_suffix_counter[suffix] += 1

# Get the 10 most common suffixes for drugs
top_10_drug_suffixes = drug_suffix_counter.most_common(10)

# Get the 10 most common suffixes for brands
top_10_brand_suffixes = brand_suffix_counter.most_common(10)

print("Top 10 Drug Suffixes:")
for suffix, count in top_10_drug_suffixes:
    print(f"{suffix}: {count}")

print("\nTop 10 Brand Suffixes:")
for suffix, count in top_10_brand_suffixes:
    print(f"{suffix}: {count}")