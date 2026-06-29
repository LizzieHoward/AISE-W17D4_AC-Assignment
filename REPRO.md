# Reproduction Guide

## Prerequisites

- **Python**: 3.9 or higher
- **uv**: Package and project manager ([installation guide](https://github.com/astral-sh/uv))
- **Internet**: Required for first run (downloads model and dataset)
- **Disk space**: ~1GB for model weights and dataset cache
- **RAM**: 2GB minimum, 4GB recommended

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd AISE-W17D4_AC-Assignment
```

### 2. Install Dependencies with uv

```bash
# Create virtual environment and install all dependencies
uv sync
```

This command will:
- Create a `.venv` directory with isolated Python environment
- Install all dependencies from `pyproject.toml`
- Lock versions for reproducibility

## Running the Prototype

### Execute Full Pipeline

```bash
uv run python -m caption_prototype.run
```

**First run**: 5-10 minutes (downloads ~500MB of models and data)
**Subsequent runs**: <1 minute (uses cached files)

### Expected Output

The command will:
1. Display progress for each of 10 test cases
2. Print a summary table to console
3. Generate output files:
   - `outputs/results.csv` - Structured test results
   - `outputs/results.json` - Machine-readable detailed results
   - `outputs/failure_examples.md` - Documented failure analysis

### Sample Console Output

```
Loading model: nlpconnect/vit-gpt2-image-captioning...
Loading dataset: COCO 2017 validation...
Running 10 test cases...

[1/10] TC-01 Clear Common Object... ✓
[2/10] TC-02 Multiple Objects... ✗ (Missed object)
[3/10] TC-03 Small Object/Background Detail... ✗ (Hallucinated)
...

Results saved to outputs/results.csv
Failure examples saved to outputs/failure_examples.md
```

## Environment Notes

### Caching

- **Model cache**: `~/.cache/huggingface/transformers/`
- **Dataset cache**: `~/.cache/huggingface/datasets/`
- **uv cache**: `.uv_cache/` (in project root)

To clear caches and re-download:
```bash
rm -rf ~/.cache/huggingface
rm -rf .uv_cache
```

### Offline Use

After the first successful run, you can work offline. Ensure:
- Model weights are cached
- Dataset samples are cached
- Do not clear cache directories

### CPU vs GPU

- **Default**: CPU inference (compatible with all systems)
- **GPU**: Automatically used if PyTorch detects CUDA
- **Performance**: GPU is 5-10x faster but not required

## Troubleshooting

### Issue: `uv` command not found

**Solution**: Install uv:
```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue: Model download fails

**Symptoms**: `requests.exceptions.ConnectionError` or timeout

**Solutions**:
1. Check internet connection
2. Retry - sometimes Hugging Face CDN is temporarily unavailable
3. Try a different network (corporate firewalls may block downloads)
4. Manual download:
   ```bash
   uv run python -c "from transformers import VisionEncoderDecoderModel; VisionEncoderDecoderModel.from_pretrained('nlpconnect/vit-gpt2-image-captioning')"
   ```

### Issue: Dataset download fails

**Symptoms**: `datasets.builder.DatasetGenerationError`

**Solutions**:
1. Retry with `uv run python -m caption_prototype.run`
2. Check available disk space (need ~500MB)
3. Manually pre-download:
   ```bash
   uv run python -c "from datasets import load_dataset; load_dataset('HuggingFaceM4/COCO', split='validation[:100]')"
   ```

### Issue: Out of memory

**Symptoms**: `RuntimeError: [enforce fail at alloc_cpu.cpp]` or similar

**Solutions**:
1. Close other applications
2. Reduce batch size (model processes one image at a time, so unlikely)
3. Use a machine with more RAM

### Issue: Import errors

**Symptoms**: `ModuleNotFoundError: No module named 'transformers'`

**Solutions**:
1. Ensure you're using `uv run`:
   ```bash
   uv run python -m caption_prototype.run
   ```
2. Re-sync dependencies:
   ```bash
   uv sync --reinstall
   ```

### Issue: No output files generated

**Symptoms**: Command completes but `outputs/` directory is empty

**Solutions**:
1. Check console for error messages
2. Verify write permissions:
   ```bash
   mkdir -p outputs
   touch outputs/test.txt
   rm outputs/test.txt
   ```
3. Run with verbose output:
   ```bash
   uv run python -m caption_prototype.run --verbose
   ```

### Issue: Results don't match expected failures

**Note**: This is expected! The prototype uses deterministic inference (fixed random seed), but model outputs can vary slightly across PyTorch versions or hardware. The failure types should be similar even if exact captions differ.

## Development Commands

### Run with verbose logging

```bash
uv run python -m caption_prototype.run --verbose
```

### Check installed packages

```bash
uv pip list
```

### Update dependencies

```bash
uv sync --upgrade
```

## Expected File Outputs

After successful run, you should see:

```
outputs/
├── results.csv          # Structured results (10 rows)
├── results.json         # Detailed machine-readable results
└── failure_examples.md  # 8+ documented failure examples
```

All files should be non-empty and contain valid data.

## Reproduction Checklist

- [ ] Python 3.9+ installed
- [ ] `uv` installed and in PATH
- [ ] Repository cloned
- [ ] `uv sync` completed successfully
- [ ] Internet connection available (first run)
- [ ] At least 1GB free disk space
- [ ] `uv run python -m caption_prototype.run` completes without errors
- [ ] `outputs/results.csv` generated and contains 10 rows
- [ ] `outputs/failure_examples.md` generated and contains 8+ examples
- [ ] Console output shows summary table

## Support

If issues persist:
1. Check that all files from repository are present
2. Verify `pyproject.toml` dependencies are correct
3. Review console output for specific error messages
4. Ensure Python version is 3.9 or higher: `python --version`
