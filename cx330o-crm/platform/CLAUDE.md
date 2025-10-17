# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

cx330o CRM Platform is a modern customer relationship management system built with a monorepo structure. The codebase is organized as an Nx workspace with multiple packages.

## Key Commands

### Development
```bash
# Start development environment (frontend + backend + worker)
yarn start

# Individual package development
npx nx start cx330o-front     # Start frontend dev server
npx nx start cx330o-server    # Start backend server
npx nx run cx330o-server:worker  # Start background worker
```

### Testing
```bash
# Run a single test file (fast)
npx jest path/to/test.test.ts --config=packages/PROJECT/jest.config.mjs

# Run all tests for a package
npx nx test cx330o-front
npx nx test cx330o-server
```

### Code Quality
```bash
# Linting
npx nx lint cx330o-front
npx nx lint cx330o-server

# Type checking
npx nx typecheck cx330o-front
npx nx typecheck cx330o-server
```

### Build
```bash
npx nx build cx330o-shared
npx nx build cx330o-front
npx nx build cx330o-server
```

### Database Operations
```bash
npx nx database:reset cx330o-server
npx nx run cx330o-server:command workspace:sync-metadata
```

## Architecture Overview

### Tech Stack
- **Frontend**: React 18, TypeScript, Jotai (state management), Linaria (styling), Vite
- **Backend**: NestJS, TypeORM, PostgreSQL, Redis, GraphQL (with GraphQL Yoga)
- **Monorepo**: Nx workspace managed with Yarn 4

### Key Development Principles
- **Functional components only** (no class components)
- **Named exports only** (no default exports)
- **Types over interfaces** (except when extending third-party interfaces)
- **No 'any' type allowed** — strict TypeScript enforced
- **Composition over inheritance**
- **No abbreviations** in variable names

### Naming Conventions
- **Variables/functions**: camelCase
- **Constants**: SCREAMING_SNAKE_CASE
- **Types/Classes**: PascalCase
- **Files/directories**: kebab-case

### Backend Architecture
- **NestJS modules** for feature organization
- **TypeORM** for database ORM with PostgreSQL
- **GraphQL** API with code-first approach
- **Redis** for caching and session management
- **BullMQ** for background job processing

### Testing Strategy
- **Test behavior, not implementation**
- **Test pyramid**: 70% unit, 20% integration, 10% E2E
- Descriptive test names: "should [behavior] when [condition]"
