import os

with open('totem-ui/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'bg-[#FAF8F5]': 'bg-zinc-950',
    'text-zinc-800': 'text-zinc-200',
    'bg-white/70': 'bg-zinc-950/80',
    'border-stone-200/80': 'border-zinc-800',
    'text-stone-900': 'text-zinc-100',
    'text-stone-500': 'text-zinc-400',
    'bg-stone-100': 'bg-zinc-800',
    'text-stone-800': 'text-zinc-100',
    'bg-stone-200/80': 'bg-zinc-700',
    'text-stone-700': 'text-zinc-300',
    'text-stone-600': 'text-zinc-400',
    'bg-stone-900': 'bg-amber-600',
    'hover:bg-stone-800': 'hover:bg-amber-700',
    'border-stone-200': 'border-zinc-800',
    'bg-white': 'bg-zinc-900',
    'text-stone-400': 'text-zinc-500',
    'bg-stone-50/70': 'bg-zinc-800/50',
    'border-stone-300': 'border-zinc-700',
    'bg-stone-50': 'bg-zinc-800',
    'border-stone-900': 'border-amber-600',
    'text-amber-300': 'text-zinc-100',
    'text-amber-600': 'text-amber-400',
    'bg-amber-50': 'bg-amber-950/50',
    'border-amber-200': 'border-amber-800',
    'text-amber-700': 'text-amber-400',
    'text-amber-900': 'text-amber-400',
    'border-t-stone-900': 'border-t-amber-600',
    'bg-amber-100': 'bg-zinc-700'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('totem-ui/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
