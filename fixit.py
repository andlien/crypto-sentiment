import yaml

with open('crypto_subreddits.yaml', 'r', encoding='utf8') as f:
    crypto = yaml.load(f)

for i in crypto.keys():
    crypto[i] = crypto[i][0]
    crypto[i]['subreddits'] = [crypto[i]['subreddit']]
    del crypto[i]['subreddit']

with open('crypto_subreddits.yaml', 'w', encoding='utf8') as f:
    f.write(yaml.dump(crypto, default_flow_style=False, allow_unicode=True))
