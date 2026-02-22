# Setup Instructions

## Install Required Packages

```bash
cd /home/ashwin/git-prjs/inaworks/inaworks/ui

# Install adapter-node and openapi-typescript
pnpm add -D @sveltejs/adapter-node openapi-typescript

# Install lucide-svelte (already have it, icons)
# pnpm add lucide-svelte
```

## Update svelte.config.js

Replace adapter-auto with adapter-node (see svelte.config.js)

## Generate API Types

```bash
# Make sure Django is running first
cd /home/ashwin/git-prjs/inaworks/inaworks
python manage.py runserver

# In another terminal, generate types
cd /home/ashwin/git-prjs/inaworks/inaworks/ui
pnpm run generate-types
```

This will create `src/lib/types/api.ts` with TypeScript types from your Django API!
