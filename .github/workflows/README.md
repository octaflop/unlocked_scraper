# GitHub Actions Workflows

This directory contains three automated workflows for CI/CD.

## Workflows Overview

### 1. `ci.yml` - Main CI/CD Pipeline 🚀

**Triggers:** Push to main/gilfree, Pull Requests, Manual
**Purpose:** Comprehensive validation and deployment

**Jobs:**
1. **lint-and-validate**
   - Validates Python syntax for all .py files
   - Checks all dependency imports
   - Uses uv for dependency management

2. **build-presentation**
   - Builds HTML and PDF presentations with Marp
   - Uploads artifacts (90-day retention)
   - Depends on lint-and-validate passing

3. **deploy-pages**
   - Deploys to GitHub Pages (main branch only)
   - Downloads built artifacts
   - Updates gh-pages branch

4. **summary**
   - Reports status of all jobs
   - Fails if any job failed

### 2. `build-presentation.yml` - Standalone Presentation Builder 📊

**Triggers:** Changes to `talk/`, Manual
**Purpose:** Build presentations independently

**Steps:**
- Checkout repository
- Setup Node.js 20
- Install Marp CLI globally (no lock file needed)
- Build HTML presentation
- Build PDF presentation
- Upload both as artifacts
- Deploy to GitHub Pages (main only)

### 3. `test-python.yml` - Python Version Testing 🐍

**Triggers:** Changes to .py files, pyproject.toml, uv.lock
**Purpose:** Test across Python versions

**Matrix:** Python 3.13, 3.14 (fail-fast disabled)

**Steps:**
- Install uv
- Setup specified Python version
- Install dependencies with `uv sync`
- Check GIL availability
- Test all imports
- Validate all Python files
- Smoke test FastAPI server

## Key Features

✅ **No package-lock.json required** - Marp CLI installed globally
✅ **Uses uv** - Fast, reliable Python dependency management
✅ **Artifact storage** - 90-day retention for presentations
✅ **Matrix testing** - Multiple Python versions
✅ **Automatic deployment** - GitHub Pages on main branch
✅ **Comprehensive validation** - All files checked

## Workflow Dependencies

```
ci.yml:
  lint-and-validate
    ↓
  build-presentation
    ↓
  deploy-pages (main only)
    ↓
  summary

build-presentation.yml:
  (independent - can run standalone)

test-python.yml:
  (independent - tests Python code)
```

## Local Testing

Test workflow syntax locally:

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
sudo apt install act  # Linux

# Run CI workflow locally
act push

# Run specific workflow
act -W .github/workflows/ci.yml

# Run specific job
act -j lint-and-validate
```

## Debugging Workflows

View workflow runs:
- Go to Actions tab in GitHub
- Click on workflow run
- Click on specific job
- Expand steps to see logs

Common issues:
1. **npm cache error**: Fixed by removing cache parameter
2. **Python version not found**: Ensure uv can install that version
3. **Import errors**: Check pyproject.toml dependencies
4. **Artifact upload fails**: Check artifact name uniqueness

## Secrets & Variables

**Required secrets:**
- `GITHUB_TOKEN` (automatically provided)

**No additional secrets needed!**

## Modifying Workflows

When making changes:
1. Test locally with `act` if possible
2. Create a PR to test in CI
3. Check all jobs pass
4. Merge when green ✅

## Workflow Status Badges

Add to README.md:

```markdown
![CI/CD](https://github.com/[username]/unlocked_scraper/workflows/CI%2FCD%20Pipeline/badge.svg)
![Build Presentation](https://github.com/[username]/unlocked_scraper/workflows/Build%20Presentation/badge.svg)
![Test Python](https://github.com/[username]/unlocked_scraper/workflows/Test%20Python%20Demos/badge.svg)
```

## Performance

Typical run times:
- **lint-and-validate**: ~1-2 minutes
- **build-presentation**: ~2-3 minutes
- **test-python** (per version): ~2-3 minutes
- **deploy-pages**: ~30 seconds

Total CI run time: ~5-7 minutes

## Future Improvements

Potential enhancements:
- [ ] Add actual unit tests with pytest
- [ ] Add code coverage reporting
- [ ] Add performance benchmarking in CI
- [ ] Cache uv dependencies between runs
- [ ] Add security scanning (Snyk, Dependabot)
- [ ] Add automatic release creation
