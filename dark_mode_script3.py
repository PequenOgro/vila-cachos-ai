import subprocess

# Read original file content directly from git
result = subprocess.run(['git', 'show', '7df3657:totem-ui/src/App.jsx'], capture_output=True, text=True, encoding='utf-8')
content = result.stdout

replacements = {
    'bg-[#FAF8F5]': 'bg-[#FAF8F5] dark:bg-zinc-950',
    'text-zinc-800': 'text-zinc-800 dark:text-zinc-200',
    'bg-white/70': 'bg-white/70 dark:bg-zinc-950/80',
    'border-stone-200/80': 'border-stone-200/80 dark:border-zinc-800',
    'text-stone-900': 'text-stone-900 dark:text-zinc-100',
    'text-stone-500': 'text-stone-500 dark:text-zinc-400',
    'bg-stone-100': 'bg-stone-100 dark:bg-zinc-800',
    'text-stone-800': 'text-stone-800 dark:text-zinc-100',
    'bg-stone-200/80': 'bg-stone-200/80 dark:bg-zinc-700',
    'text-stone-700': 'text-stone-700 dark:text-zinc-300',
    'text-stone-600': 'text-stone-600 dark:text-zinc-400',
    'bg-stone-900': 'bg-stone-900 dark:bg-amber-600',
    'hover:bg-stone-800': 'hover:bg-stone-800 dark:hover:bg-amber-700',
    'border-stone-200': 'border-stone-200 dark:border-zinc-800',
    'bg-white': 'bg-white dark:bg-zinc-900',
    'text-stone-400': 'text-stone-400 dark:text-zinc-500',
    'bg-stone-50/70': 'bg-stone-50/70 dark:bg-zinc-800/50',
    'border-stone-300': 'border-stone-300 dark:border-zinc-700',
    'bg-stone-50': 'bg-stone-50 dark:bg-zinc-800',
    'border-stone-900': 'border-stone-900 dark:border-amber-600',
    'text-amber-300': 'text-amber-300 dark:text-zinc-100',
    'text-amber-600': 'text-amber-600 dark:text-amber-400',
    'bg-amber-50': 'bg-amber-50 dark:bg-amber-950/50',
    'border-amber-200': 'border-amber-200 dark:border-amber-800',
    'text-amber-700': 'text-amber-700 dark:text-amber-400',
    'text-amber-900': 'text-amber-900 dark:text-amber-400',
    'border-t-stone-900': 'border-t-stone-900 dark:border-t-amber-600',
    'bg-amber-100': 'bg-amber-100 dark:bg-zinc-700'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('totem-ui/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
