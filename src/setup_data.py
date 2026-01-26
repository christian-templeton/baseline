"""Auto-download tau2 benchmark data on first import."""
import os
import shutil
import tarfile
import tempfile
import urllib.request
def ensure_tau2_data():
    """Download and install tau2 data if missing."""
    import tau2
    tau2_dir = os.path.dirname(tau2.__file__)
    domains_dir = os.path.join(tau2_dir, "domains")
    
    if os.path.exists(domains_dir):
        return  # Already installed
    
    print("Downloading tau2 benchmark data...")
    url = "https://github.com/sierra-research/tau2-bench/archive/refs/heads/main.tar.gz"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tarball = os.path.join(tmpdir, "tau2.tar.gz")
        urllib.request.urlretrieve(url, tarball)
        
        with tarfile.open(tarball) as tar:
            tar.extractall(tmpdir)
        
        src = os.path.join(tmpdir, "tau2-bench-main", "src", "tau2", "domains")
        shutil.copytree(src, domains_dir)
    
    print("tau2 data installed successfully!")
ensure_tau2_data()
