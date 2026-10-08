#!/bin/bash
cd ~/workspace/affiliate-site/hidden_files/batch4-work
python3 << 'PYEOF'
import json
from collections import Counter
results = json.load(open('extracted.json'))
imgs = Counter(r['image'] for r in results if r.get('image') and 'temu-avi' not in r['image'])
common = imgs.most_common(1)[0][0]
failed = [r['link'] for r in results if r.get('image') == common]
open('/tmp/refetch_all.txt', 'w').write('\n'.join(failed))
print(f"To refetch: {len(failed)}")
PYEOF
mkdir -p refetch_full
count=0
while read link; do
  code=$(echo "$link" | md5sum | cut -c1-12)
  curl -sL --max-redirs 5 \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
    -H "Accept-Language: en-US,en;q=0.5" \
    -H "Sec-Ch-Ua: \"Chromium\";v=\"126\", \"Not-A.Brand\";v=\"99\"" \
    -H "Sec-Ch-Ua-Mobile: ?0" \
    -H "Sec-Fetch-Dest: document" \
    -H "Sec-Fetch-Mode: navigate" \
    --compressed --max-time 60 -o "refetch_full/${code}.html" "$link" 2>/dev/null
  count=$((count+1))
  if [ $((count % 10)) -eq 0 ]; then echo "Progress: $count"; fi
  sleep 5
done < /tmp/refetch_all.txt
echo "DONE: $count fetched"
