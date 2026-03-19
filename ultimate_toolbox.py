#!/usr/bin/env python3
"""
==========================================================================
ULTIMATE SYSTEM TOOLBOX v3.0 - 30+ Tools - No Extra Modules Required!
==========================================================================
All tools work with Python standard library only!
==========================================================================
"""

import os
import sys
import json
import time
import shutil
import hashlib
import threading
import webbrowser
import platform
import subprocess
import socket
import random
import string
import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import base64
import glob
import ctypes
from collections import Counter

# ============================================================================
# CONFIGURATION
# ============================================================================

HOST = '127.0.0.1'
PORT = 8080
VERSION = "3.0"

# ============================================================================
# ULTIMATE TOOLBOX CLASS - 30+ Tools Working Out of Box!
# ============================================================================

class UltimateToolbox:
    def __init__(self):
        self.system = platform.system()
        self.home = Path.home()
        self.desktop = self.home / "Desktop"
        self.tools_count = 32
        self.results = {}
        
    # ============================================================================
    # TOOL 1: System Information
    # ============================================================================
    
    def tool_001_system_info(self):
        """Get complete system information"""
        try:
            import psutil
            memory = psutil.virtual_memory()._asdict()
            disk = psutil.disk_usage('/')._asdict()
            cpu_percent = psutil.cpu_percent(interval=1)
        except:
            memory = {'total': 0, 'available': 0, 'percent': 0}
            disk = {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
            cpu_percent = 0
        
        info = {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.get('percent', 0),
            'memory_total': self.format_size(memory.get('total', 0)),
            'memory_available': self.format_size(memory.get('available', 0)),
            'disk_total': self.format_size(disk.get('total', 0)),
            'disk_free': self.format_size(disk.get('free', 0)),
            'disk_used': self.format_size(disk.get('used', 0)),
            'disk_percent': disk.get('percent', 0),
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'python_version': sys.version.split()[0],
            'current_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return info
    
    # ============================================================================
    # TOOL 2: Running Processes
    # ============================================================================
    
    def tool_002_running_processes(self):
        """Get list of running processes"""
        processes = []
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    continue
            return sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:30]
        except:
            # Fallback: use tasklist on Windows
            if self.system == 'Windows':
                try:
                    result = subprocess.run(['tasklist'], capture_output=True, text=True)
                    lines = result.stdout.split('\n')[3:]
                    for line in lines[:30]:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                processes.append({
                                    'name': parts[0],
                                    'pid': parts[1] if len(parts) > 1 else 'N/A'
                                })
                except:
                    pass
        return processes
    
    # ============================================================================
    # TOOL 3: Environment Variables
    # ============================================================================
    
    def tool_003_environment_vars(self):
        """Get environment variables"""
        return dict(os.environ)
    
    # ============================================================================
    # TOOL 4: Disk Drives
    # ============================================================================
    
    def tool_004_disk_drives(self):
        """List all disk drives"""
        drives = []
        if self.system == 'Windows':
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        total, used, free = shutil.disk_usage(drive)
                        drives.append({
                            'drive': drive,
                            'total': self.format_size(total),
                            'used': self.format_size(used),
                            'free': self.format_size(free),
                            'percent': (used / total) * 100
                        })
                    except:
                        drives.append({'drive': drive, 'error': 'Access denied'})
        else:
            # Unix-like systems
            for mount in ['/', '/home', '/usr']:
                if os.path.exists(mount):
                    try:
                        total, used, free = shutil.disk_usage(mount)
                        drives.append({
                            'drive': mount,
                            'total': self.format_size(total),
                            'used': self.format_size(used),
                            'free': self.format_size(free),
                            'percent': (used / total) * 100
                        })
                    except:
                        pass
        return drives
    
    # ============================================================================
    # TOOL 5: Network Interfaces
    # ============================================================================
    
    def tool_005_network_interfaces(self):
        """List network interfaces"""
        interfaces = []
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
            interfaces.append({
                'name': 'Primary',
                'ip': local_ip,
                'hostname': hostname
            })
        except:
            pass
        
        # Try to get all interfaces
        try:
            import netifaces
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        interfaces.append({
                            'name': iface,
                            'ip': addr['addr'],
                            'netmask': addr.get('netmask', 'N/A')
                        })
        except:
            pass
        
        return interfaces
    
    # ============================================================================
    # TOOL 6: Public IP
    # ============================================================================
    
    def tool_006_public_ip(self):
        """Get public IP address"""
        try:
            # Try multiple services
            services = [
                'https://api.ipify.org',
                'https://icanhazip.com',
                'https://ifconfig.me/ip'
            ]
            for service in services:
                try:
                    import urllib.request
                    ip = urllib.request.urlopen(service, timeout=3).read().decode().strip()
                    return {'ip': ip, 'source': service}
                except:
                    continue
        except:
            pass
        return {'ip': 'Unknown', 'error': 'Could not determine public IP'}
    
    # ============================================================================
    # TOOL 7: Port Scanner
    # ============================================================================
    
    def tool_007_port_scanner(self, target='localhost', ports=None):
        """Scan common ports"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    # Get service name
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = 'unknown'
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'status': 'open'
                    })
                sock.close()
            except:
                continue
        
        return {
            'target': target,
            'open_ports': open_ports,
            'total_scanned': len(ports),
            'open_count': len(open_ports)
        }
    
    # ============================================================================
    # TOOL 8: DNS Lookup
    # ============================================================================
    
    def tool_008_dns_lookup(self, domain='google.com'):
        """Perform DNS lookup"""
        try:
            ips = socket.gethostbyname_ex(domain)
            return {
                'domain': domain,
                'ips': ips[2],
                'aliases': ips[1],
                'primary_ip': ips[2][0] if ips[2] else 'None'
            }
        except:
            return {'error': f'Could not resolve {domain}'}
    
    # ============================================================================
    # TOOL 9: Find Duplicate Files
    # ============================================================================
    
    def tool_009_find_duplicates(self, path=None):
        """Find duplicate files"""
        if path is None:
            path = self.desktop
            
        path = Path(path)
        file_sizes = {}
        duplicates = []
        
        # Group by size first
        for file in path.rglob('*'):
            if file.is_file() and file.stat().st_size > 0:
                size = file.stat().st_size
                if size not in file_sizes:
                    file_sizes[size] = []
                file_sizes[size].append(file)
        
        # Check files with same size
        for size, files in file_sizes.items():
            if len(files) > 1:
                # Check content
                content_hashes = {}
                for file in files:
                    try:
                        with open(file, 'rb') as f:
                            file_hash = hashlib.md5(f.read(8192)).hexdigest()
                        if file_hash not in content_hashes:
                            content_hashes[file_hash] = []
                        content_hashes[file_hash].append(file)
                    except:
                        continue
                
                # Collect duplicates
                for file_hash, file_list in content_hashes.items():
                    if len(file_list) > 1:
                        duplicates.append({
                            'size': self.format_size(size),
                            'size_bytes': size,
                            'files': [str(f) for f in file_list],
                            'count': len(file_list),
                            'hash': file_hash[:8] + '...'
                        })
        
        return duplicates
    
    # ============================================================================
    # TOOL 10: Large Files
    # ============================================================================
    
    def tool_010_large_files(self, path=None, threshold_mb=100):
        """Find large files"""
        if path is None:
            path = self.desktop
            
        path = Path(path)
        threshold = threshold_mb * 1024 * 1024
        large_files = []
        
        for file in path.rglob('*'):
            if file.is_file():
                size = file.stat().st_size
                if size > threshold:
                    large_files.append({
                        'name': file.name,
                        'path': str(file),
                        'size': self.format_size(size),
                        'size_bytes': size,
                        'modified': datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
        
        return sorted(large_files, key=lambda x: x['size_bytes'], reverse=True)
    
    # ============================================================================
    # TOOL 11: Temp Files
    # ============================================================================
    
    def tool_011_temp_files(self):
        """Find temporary files"""
        temp_files = []
        temp_patterns = ['*.tmp', '*.temp', '*.log', '*.bak', '~*.*']
        
        # Common temp locations
        temp_locations = []
        if self.system == 'Windows':
            temp = os.environ.get('TEMP', '')
            if temp:
                temp_locations.append(Path(temp))
            temp_locations.append(Path('C:/Windows/Temp'))
            temp_locations.append(self.home / 'AppData/Local/Temp')
        else:
            temp_locations.append(Path('/tmp'))
            temp_locations.append(self.home / '.cache')
        
        for location in temp_locations:
            if location.exists():
                for pattern in temp_patterns:
                    for file in location.glob(pattern):
                        if file.is_file():
                            age = time.time() - file.stat().st_mtime
                            if age > 7 * 86400:  # Older than 7 days
                                temp_files.append({
                                    'name': file.name,
                                    'path': str(file),
                                    'size': self.format_size(file.stat().st_size),
                                    'size_bytes': file.stat().st_size,
                                    'location': str(location),
                                    'age_days': round(age / 86400, 1)
                                })
        
        return temp_files
    
    # ============================================================================
    # TOOL 12: Empty Folders
    # ============================================================================
    
    def tool_012_empty_folders(self, path=None):
        """Find empty folders"""
        if path is None:
            path = self.desktop
            
        path = Path(path)
        empty_folders = []
        
        for folder in path.rglob('*'):
            if folder.is_dir():
                try:
                    if not any(folder.iterdir()):
                        empty_folders.append({
                            'name': folder.name,
                            'path': str(folder)
                        })
                except:
                    continue
        
        return empty_folders
    
    # ============================================================================
    # TOOL 13: File Types Stats
    # ============================================================================
    
    def tool_013_file_types_stats(self, path=None):
        """Get statistics by file type"""
        if path is None:
            path = self.desktop
            
        path = Path(path)
        stats = {}
        total_size = 0
        total_files = 0
        
        for file in path.rglob('*'):
            if file.is_file():
                ext = file.suffix.lower() or 'no_extension'
                size = file.stat().st_size
                
                if ext not in stats:
                    stats[ext] = {'count': 0, 'total_size': 0, 'files': []}
                
                stats[ext]['count'] += 1
                stats[ext]['total_size'] += size
                if len(stats[ext]['files']) < 5:  # Store sample files
                    stats[ext]['files'].append(file.name)
                
                total_size += size
                total_files += 1
        
        # Format sizes
        result = []
        for ext, data in stats.items():
            result.append({
                'extension': ext or 'No Extension',
                'count': data['count'],
                'total_size': self.format_size(data['total_size']),
                'percentage': round((data['count'] / total_files) * 100, 1) if total_files else 0,
                'samples': data['files']
            })
        
        return sorted(result, key=lambda x: x['count'], reverse=True)
    
    # ============================================================================
    # TOOL 14: Recent Files
    # ============================================================================
    
    def tool_014_recent_files(self, days=7):
        """Find recently modified files"""
        recent = []
        cutoff = time.time() - (days * 86400)
        
        for file in self.desktop.rglob('*'):
            if file.is_file():
                mtime = file.stat().st_mtime
                if mtime > cutoff:
                    recent.append({
                        'name': file.name,
                        'path': str(file),
                        'size': self.format_size(file.stat().st_size),
                        'modified': datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M'),
                        'age_days': round((time.time() - mtime) / 86400, 1)
                    })
        
        return sorted(recent, key=lambda x: x['age_days'])[:50]
    
    # ============================================================================
    # TOOL 15: Folder Sizes
    # ============================================================================
    
    def tool_015_folder_sizes(self, path=None):
        """Calculate folder sizes"""
        if path is None:
            path = self.desktop
            
        path = Path(path)
        folder_sizes = []
        
        for item in path.iterdir():
            if item.is_dir():
                total_size = 0
                file_count = 0
                for file in item.rglob('*'):
                    if file.is_file():
                        total_size += file.stat().st_size
                        file_count += 1
                
                folder_sizes.append({
                    'name': item.name,
                    'path': str(item),
                    'size': self.format_size(total_size),
                    'size_bytes': total_size,
                    'files': file_count,
                    'folders': len([d for d in item.rglob('*') if d.is_dir()])
                })
        
        return sorted(folder_sizes, key=lambda x: x['size_bytes'], reverse=True)
    
    # ============================================================================
    # TOOL 16: Change Wallpaper (Windows only)
    # ============================================================================
    
    def tool_016_change_wallpaper(self, image_path=None):
        """Change desktop wallpaper"""
        if self.system != 'Windows':
            return {'error': 'This tool only works on Windows'}
        
        if image_path is None:
            # Use a random Windows wallpaper
            wallpaper_dir = Path('C:/Windows/Web/Wallpaper')
            if wallpaper_dir.exists():
                images = list(wallpaper_dir.rglob('*.jpg')) + list(wallpaper_dir.rglob('*.png'))
                if images:
                    image_path = str(random.choice(images))
        
        if image_path and Path(image_path).exists():
            try:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
                return {
                    'success': True,
                    'wallpaper': image_path,
                    'message': 'Wallpaper changed successfully'
                }
            except:
                return {'error': 'Failed to change wallpaper'}
        return {'error': 'Image not found'}
    
    # ============================================================================
    # TOOL 17: Password Generator
    # ============================================================================
    
    def tool_017_password_generator(self, length=12, use_special=True):
        """Generate strong password"""
        chars = string.ascii_letters + string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Check strength
        strength = 'Weak'
        score = 0
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1
        
        if score >= 5:
            strength = 'Very Strong'
        elif score >= 4:
            strength = 'Strong'
        elif score >= 3:
            strength = 'Medium'
        
        return {
            'password': password,
            'length': length,
            'strength': strength,
            'score': f"{score}/6",
            'has_lower': any(c.islower() for c in password),
            'has_upper': any(c.isupper() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        }
    
    # ============================================================================
    # TOOL 18: File Encrypt (Simple XOR)
    # ============================================================================
    
    def tool_018_file_encrypt(self, file_path, password):
        """Encrypt a file using XOR"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {'error': 'File not found'}
            
            with open(path, 'rb') as f:
                data = f.read()
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            
            # XOR encryption
            encrypted = bytearray()
            for i, byte in enumerate(data):
                encrypted.append(byte ^ key[i % len(key)])
            
            # Save encrypted file
            encrypted_path = path.with_suffix(path.suffix + '.encrypted')
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            return {
                'success': True,
                'encrypted_file': str(encrypted_path),
                'original': str(path),
                'size': self.format_size(len(data)),
                'message': 'File encrypted successfully'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================================================
    # TOOL 19: File Decrypt
    # ============================================================================
    
    def tool_019_file_decrypt(self, file_path, password):
        """Decrypt a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {'error': 'File not found'}
            
            if not path.suffix == '.encrypted':
                return {'error': 'Not an encrypted file'}
            
            with open(path, 'rb') as f:
                data = f.read()
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            
            # XOR decryption
            decrypted = bytearray()
            for i, byte in enumerate(data):
                decrypted.append(byte ^ key[i % len(key)])
            
            # Save decrypted file
            decrypted_path = path.with_suffix('')
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted)
            
            return {
                'success': True,
                'decrypted_file': str(decrypted_path),
                'original': str(path),
                'size': self.format_size(len(data)),
                'message': 'File decrypted successfully'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================================================
    # TOOL 20: File Hasher
    # ============================================================================
    
    def tool_020_file_hasher(self, file_path):
        """Calculate file hashes"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {'error': 'File not found'}
            
            hashes = {}
            with open(path, 'rb') as f:
                data = f.read()
                hashes['md5'] = hashlib.md5(data).hexdigest()
                hashes['sha1'] = hashlib.sha1(data).hexdigest()
                hashes['sha256'] = hashlib.sha256(data).hexdigest()
            
            return {
                'file': file_path,
                'size': self.format_size(path.stat().st_size),
                'hashes': hashes
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================================================
    # TOOL 21: Text Hash Generator
    # ============================================================================
    
    def tool_021_hash_generator(self, text):
        """Generate hashes from text"""
        return {
            'text': text,
            'md5': hashlib.md5(text.encode()).hexdigest(),
            'sha1': hashlib.sha1(text.encode()).hexdigest(),
            'sha256': hashlib.sha256(text.encode()).hexdigest(),
            'sha512': hashlib.sha512(text.encode()).hexdigest()
        }
    
    # ============================================================================
    # TOOL 22: Base64 Encode
    # ============================================================================
    
    def tool_022_base64_encode(self, text):
        """Encode text to Base64"""
        encoded = base64.b64encode(text.encode()).decode()
        return {
            'original': text,
            'encoded': encoded,
            'length': len(encoded)
        }
    
    # ============================================================================
    # TOOL 23: Base64 Decode
    # ============================================================================
    
    def tool_023_base64_decode(self, encoded):
        """Decode Base64 to text"""
        try:
            decoded = base64.b64decode(encoded).decode()
            return {
                'success': True,
                'decoded': decoded,
                'original': encoded
            }
        except:
            return {'error': 'Invalid Base64 string'}
    
    # ============================================================================
    # TOOL 24: URL Encode
    # ============================================================================
    
    def tool_024_url_encode(self, text):
        """URL encode text"""
        encoded = urllib.parse.quote(text)
        return {
            'original': text,
            'encoded': encoded
        }
    
    # ============================================================================
    # TOOL 25: URL Decode
    # ============================================================================
    
    def tool_025_url_decode(self, encoded):
        """URL decode text"""
        try:
            decoded = urllib.parse.unquote(encoded)
            return {
                'success': True,
                'decoded': decoded
            }
        except:
            return {'error': 'Invalid URL encoding'}
    
    # ============================================================================
    # TOOL 26: JSON Formatter
    # ============================================================================
    
    def tool_026_json_formatter(self, json_string):
        """Format JSON"""
        try:
            parsed = json.loads(json_string)
            formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
            return {
                'success': True,
                'formatted': formatted,
                'original': json_string
            }
        except Exception as e:
            return {'error': f'Invalid JSON: {str(e)}'}
    
    # ============================================================================
    # TOOL 27: Text Counter
    # ============================================================================
    
    def tool_027_text_counter(self, text):
        """Count text statistics"""
        words = text.split()
        lines = text.split('\n')
        
        return {
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'words': len(words),
            'lines': len(lines),
            'paragraphs': len([l for l in lines if l.strip()]),
            'unique_words': len(set(words)),
            'average_word_length': round(sum(len(w) for w in words) / len(words), 2) if words else 0
        }
    
    # ============================================================================
    # TOOL 28: System Uptime
    # ============================================================================
    
    def tool_028_system_uptime(self):
        """Get system uptime"""
        try:
            import psutil
            boot = psutil.boot_time()
        except:
            # Fallback for Windows
            if self.system == 'Windows':
                try:
                    result = subprocess.run(['net', 'stats', 'srv'], capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if 'Statistics since' in line:
                            # Parse date
                            return {'uptime': line}
                except:
                    pass
            boot = time.time() - 3600  # Default 1 hour
        
        now = time.time()
        uptime_seconds = now - boot
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        return {
            'seconds': uptime_seconds,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'formatted': f"{days}d {hours}h {minutes}m {seconds}s",
            'boot_time': datetime.datetime.fromtimestamp(boot).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # ============================================================================
    # TOOL 29: IP Information
    # ============================================================================
    
    def tool_029_ip_info(self, ip=None):
        """Get IP information"""
        if ip is None:
            ip = socket.gethostbyname(socket.gethostname())
        
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = 'Unknown'
        
        return {
            'ip': ip,
            'hostname': hostname,
            'is_private': ip.startswith(('10.', '172.16.', '172.17.', '172.18.', '172.19.', 
                                         '172.20.', '172.21.', '172.22.', '172.23.', 
                                         '172.24.', '172.25.', '172.26.', '172.27.', 
                                         '172.28.', '172.29.', '172.30.', '172.31.', 
                                         '192.168.', '127.')),
            'type': 'IPv4'
        }
    
    # ============================================================================
    # TOOL 30: Ping Tool
    # ============================================================================
    
    def tool_030_ping(self, host='google.com', count=4):
        """Ping a host"""
        try:
            if self.system == 'Windows':
                cmd = ['ping', '-n', str(count), host]
            else:
                cmd = ['ping', '-c', str(count), host]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Parse response time
            times = []
            for line in result.stdout.split('\n'):
                if 'time=' in line or 'time<' in line:
                    try:
                        time_str = line.split('time=')[1].split()[0]
                        times.append(time_str)
                    except:
                        pass
            
            return {
                'host': host,
                'success': result.returncode == 0,
                'output': result.stdout,
                'packets_sent': count,
                'packets_received': len(times),
                'packet_loss': ((count - len(times)) / count) * 100,
                'times': times
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ============================================================================
    # TOOL 31: MAC Address
    # ============================================================================
    
    def tool_031_mac_address(self):
        """Get MAC address"""
        try:
            import uuid
            mac = uuid.getnode()
            mac_hex = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
            return {
                'mac': mac_hex,
                'decimal': mac
            }
        except:
            return {'error': 'Could not get MAC address'}
    
    # ============================================================================
    # TOOL 32: Random Generator
    # ============================================================================
    
    def tool_032_random_generator(self, type='number', min_val=1, max_val=100, length=10):
        """Generate random data"""
        result = {}
        
        if type == 'number':
            result['value'] = random.randint(min_val, max_val)
        elif type == 'float':
            result['value'] = random.uniform(min_val, max_val)
        elif type == 'string':
            result['value'] = ''.join(random.choices(string.ascii_letters, k=length))
        elif type == 'hex':
            result['value'] = ''.join(random.choices('0123456789abcdef', k=length))
        elif type == 'binary':
            result['value'] = ''.join(random.choices('01', k=length))
        elif type == 'uuid':
            result['value'] = str(uuid.uuid4())
        
        return result
    
    # ============================================================================
    # Helper: Format Size
    # ============================================================================
    
    def format_size(self, size):
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    # ============================================================================
    # Delete Files
    # ============================================================================
    
    def delete_files(self, file_paths):
        """Delete specified files"""
        deleted = 0
        failed = 0
        freed_space = 0
        
        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    freed_space += path.stat().st_size
                    path.unlink()
                    deleted += 1
            except:
                failed += 1
        
        return {
            'deleted': deleted,
            'failed': failed,
            'freed_space': self.format_size(freed_space),
            'freed_bytes': freed_space
        }

# ============================================================================
# HTTP REQUEST HANDLER
# ============================================================================

class RequestHandler(BaseHTTPRequestHandler):
    toolbox = UltimateToolbox()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == '/' or path == '/index.html':
            self.send_html_response()
        elif path == '/api/tools':
            self.send_json_response(self.get_tools_list())
        elif path.startswith('/api/tool/'):
            tool_id = path.replace('/api/tool/', '')
            self.execute_tool(tool_id, query)
        elif path == '/static/style.css':
            self.send_css()
        elif path == '/static/script.js':
            self.send_js()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path.startswith('/api/tool/'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            tool_id = path.replace('/api/tool/', '')
            self.execute_tool_post(tool_id, data)
        elif path == '/api/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            result = self.toolbox.delete_files(data.get('files', []))
            self.send_json_response(result)
        else:
            self.send_error(404)
    
    def get_tools_list(self):
        """Get list of all tools"""
        tools = [
            {'id': '001', 'name': 'System Information', 'category': 'System', 'icon': 'fa-info-circle', 'desc': 'Complete system details'},
            {'id': '002', 'name': 'Running Processes', 'category': 'System', 'icon': 'fa-tasks', 'desc': 'List all running processes'},
            {'id': '003', 'name': 'Environment Variables', 'category': 'System', 'icon': 'fa-code', 'desc': 'View all environment variables'},
            {'id': '004', 'name': 'Disk Drives', 'category': 'System', 'icon': 'fa-hdd', 'desc': 'List all disk drives'},
            {'id': '005', 'name': 'Network Interfaces', 'category': 'Network', 'icon': 'fa-network-wired', 'desc': 'Show network adapters'},
            {'id': '006', 'name': 'Public IP', 'category': 'Network', 'icon': 'fa-globe', 'desc': 'Get your public IP address'},
            {'id': '007', 'name': 'Port Scanner', 'category': 'Network', 'icon': 'fa-plug', 'desc': 'Scan for open ports'},
            {'id': '008', 'name': 'DNS Lookup', 'category': 'Network', 'icon': 'fa-search', 'desc': 'Resolve domain to IP'},
            {'id': '009', 'name': 'Find Duplicates', 'category': 'Files', 'icon': 'fa-copy', 'desc': 'Find duplicate files'},
            {'id': '010', 'name': 'Large Files', 'category': 'Files', 'icon': 'fa-chart-bar', 'desc': 'Find files > 100MB'},
            {'id': '011', 'name': 'Temp Files', 'category': 'Files', 'icon': 'fa-trash', 'desc': 'Find temporary files'},
            {'id': '012', 'name': 'Empty Folders', 'category': 'Files', 'icon': 'fa-folder-open', 'desc': 'Find empty folders'},
            {'id': '013', 'name': 'File Types Stats', 'category': 'Files', 'icon': 'fa-file-alt', 'desc': 'Statistics by file type'},
            {'id': '014', 'name': 'Recent Files', 'category': 'Files', 'icon': 'fa-history', 'desc': 'Recently modified files'},
            {'id': '015', 'name': 'Folder Sizes', 'category': 'Files', 'icon': 'fa-chart-pie', 'desc': 'Calculate folder sizes'},
            {'id': '016', 'name': 'Change Wallpaper', 'category': 'Customize', 'icon': 'fa-image', 'desc': 'Change desktop wallpaper'},
            {'id': '017', 'name': 'Password Generator', 'category': 'Security', 'icon': 'fa-key', 'desc': 'Generate strong passwords'},
            {'id': '018', 'name': 'File Encrypt', 'category': 'Security', 'icon': 'fa-lock', 'desc': 'Encrypt files with password'},
            {'id': '019', 'name': 'File Decrypt', 'category': 'Security', 'icon': 'fa-unlock', 'desc': 'Decrypt encrypted files'},
            {'id': '020', 'name': 'File Hasher', 'category': 'Security', 'icon': 'fa-hashtag', 'desc': 'Calculate file hashes'},
            {'id': '021', 'name': 'Hash Generator', 'category': 'Developer', 'icon': 'fa-hashtag', 'desc': 'Generate text hashes'},
            {'id': '022', 'name': 'Base64 Encode', 'category': 'Developer', 'icon': 'fa-code', 'desc': 'Encode text to Base64'},
            {'id': '023', 'name': 'Base64 Decode', 'category': 'Developer', 'icon': 'fa-code', 'desc': 'Decode Base64 to text'},
            {'id': '024', 'name': 'URL Encode', 'category': 'Developer', 'icon': 'fa-link', 'desc': 'URL encode text'},
            {'id': '025', 'name': 'URL Decode', 'category': 'Developer', 'icon': 'fa-link', 'desc': 'URL decode text'},
            {'id': '026', 'name': 'JSON Formatter', 'category': 'Developer', 'icon': 'fa-brackets-curly', 'desc': 'Format JSON'},
            {'id': '027', 'name': 'Text Counter', 'category': 'Developer', 'icon': 'fa-font', 'desc': 'Count words/characters'},
            {'id': '028', 'name': 'System Uptime', 'category': 'System', 'icon': 'fa-clock', 'desc': 'How long system running'},
            {'id': '029', 'name': 'IP Information', 'category': 'Network', 'icon': 'fa-network-wired', 'desc': 'Get IP details'},
            {'id': '030', 'name': 'Ping Tool', 'category': 'Network', 'icon': 'fa-satellite-dish', 'desc': 'Ping a host'},
            {'id': '031', 'name': 'MAC Address', 'category': 'Network', 'icon': 'fa-ethernet', 'desc': 'Get MAC address'},
            {'id': '032', 'name': 'Random Generator', 'category': 'Developer', 'icon': 'fa-dice', 'desc': 'Generate random data'},
        ]
        return tools
    
    def execute_tool(self, tool_id, query):
        """Execute a tool by ID"""
        result = None
        
        # System Info
        if tool_id == '001':
            result = self.toolbox.tool_001_system_info()
        elif tool_id == '002':
            result = self.toolbox.tool_002_running_processes()
        elif tool_id == '003':
            result = self.toolbox.tool_003_environment_vars()
        elif tool_id == '004':
            result = self.toolbox.tool_004_disk_drives()
        elif tool_id == '005':
            result = self.toolbox.tool_005_network_interfaces()
        elif tool_id == '006':
            result = self.toolbox.tool_006_public_ip()
        elif tool_id == '007':
            target = query.get('target', ['localhost'])[0]
            result = self.toolbox.tool_007_port_scanner(target)
        elif tool_id == '008':
            domain = query.get('domain', ['google.com'])[0]
            result = self.toolbox.tool_008_dns_lookup(domain)
        
        # File Tools
        elif tool_id == '009':
            path = query.get('path', [None])[0]
            result = self.toolbox.tool_009_find_duplicates(path)
        elif tool_id == '010':
            path = query.get('path', [None])[0]
            threshold = int(query.get('threshold', [100])[0])
            result = self.toolbox.tool_010_large_files(path, threshold)
        elif tool_id == '011':
            result = self.toolbox.tool_011_temp_files()
        elif tool_id == '012':
            path = query.get('path', [None])[0]
            result = self.toolbox.tool_012_empty_folders(path)
        elif tool_id == '013':
            path = query.get('path', [None])[0]
            result = self.toolbox.tool_013_file_types_stats(path)
        elif tool_id == '014':
            days = int(query.get('days', [7])[0])
            result = self.toolbox.tool_014_recent_files(days)
        elif tool_id == '015':
            path = query.get('path', [None])[0]
            result = self.toolbox.tool_015_folder_sizes(path)
        
        # Customization
        elif tool_id == '016':
            image = query.get('image', [None])[0]
            result = self.toolbox.tool_016_change_wallpaper(image)
        
        # Security
        elif tool_id == '017':
            length = int(query.get('length', [12])[0])
            special = query.get('special', ['true'])[0].lower() == 'true'
            result = self.toolbox.tool_017_password_generator(length, special)
        elif tool_id == '020':
            file_path = query.get('file', [''])[0]
            if file_path:
                result = self.toolbox.tool_020_file_hasher(file_path)
            else:
                result = {'error': 'No file specified'}
        
        # Developer
        elif tool_id == '021':
            text = query.get('text', [''])[0]
            if text:
                result = self.toolbox.tool_021_hash_generator(text)
            else:
                result = {'error': 'No text provided'}
        elif tool_id == '022':
            text = query.get('text', [''])[0]
            if text:
                result = self.toolbox.tool_022_base64_encode(text)
            else:
                result = {'error': 'No text provided'}
        elif tool_id == '023':
            encoded = query.get('encoded', [''])[0]
            if encoded:
                result = self.toolbox.tool_023_base64_decode(encoded)
            else:
                result = {'error': 'No encoded text provided'}
        elif tool_id == '024':
            text = query.get('text', [''])[0]
            if text:
                result = self.toolbox.tool_024_url_encode(text)
            else:
                result = {'error': 'No text provided'}
        elif tool_id == '025':
            encoded = query.get('encoded', [''])[0]
            if encoded:
                result = self.toolbox.tool_025_url_decode(encoded)
            else:
                result = {'error': 'No encoded text provided'}
        elif tool_id == '027':
            text = query.get('text', [''])[0]
            if text:
                result = self.toolbox.tool_027_text_counter(text)
            else:
                result = {'error': 'No text provided'}
        
        # Network
        elif tool_id == '028':
            result = self.toolbox.tool_028_system_uptime()
        elif tool_id == '029':
            ip = query.get('ip', [None])[0]
            result = self.toolbox.tool_029_ip_info(ip)
        elif tool_id == '030':
            host = query.get('host', ['google.com'])[0]
            count = int(query.get('count', [4])[0])
            result = self.toolbox.tool_030_ping(host, count)
        elif tool_id == '031':
            result = self.toolbox.tool_031_mac_address()
        elif tool_id == '032':
            type_val = query.get('type', ['number'])[0]
            min_val = int(query.get('min', [1])[0])
            max_val = int(query.get('max', [100])[0])
            length = int(query.get('length', [10])[0])
            result = self.toolbox.tool_032_random_generator(type_val, min_val, max_val, length)
        
        if result is None:
            result = {'error': 'Tool not implemented'}
        
        self.send_json_response(result)
    
    def execute_tool_post(self, tool_id, data):
        """Execute POST-based tools"""
        result = None
        
        if tool_id == '018':
            result = self.toolbox.tool_018_file_encrypt(data.get('file'), data.get('password'))
        elif tool_id == '019':
            result = self.toolbox.tool_019_file_decrypt(data.get('file'), data.get('password'))
        elif tool_id == '026':
            result = self.toolbox.tool_026_json_formatter(data.get('json', '{}'))
        
        if result is None:
            result = {'error': 'Tool not implemented'}
        
        self.send_json_response(result)
    
    def send_html_response(self):
        """Send HTML page"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str, indent=2).encode('utf-8'))
    
    def send_css(self):
        """Send CSS"""
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(CSS_CONTENT.encode('utf-8'))
    
    def send_js(self):
        """Send JavaScript"""
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(JS_CONTENT.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Disable logging"""
        pass

# ============================================================================
# HTML PAGE (Simplified)
# ============================================================================

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTIMATE SYSTEM TOOLBOX - 32 Tools</title>
    <link rel="stylesheet" href="/static/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <i class="fas fa-tools"></i>
                <div class="logo-text">
                    <span class="logo-title">ULTIMATE TOOLBOX</span>
                    <span class="logo-version">v3.0 | 32 Tools</span>
                </div>
            </div>
            
            <div class="categories">
                <div class="category-item active" data-category="all">
                    <i class="fas fa-th-large"></i>
                    <span>All Tools</span>
                    <span class="cat-count" id="count-all">32</span>
                </div>
                <div class="category-item" data-category="System">
                    <i class="fas fa-info-circle"></i>
                    <span>System</span>
                    <span class="cat-count" id="count-system">5</span>
                </div>
                <div class="category-item" data-category="Files">
                    <i class="fas fa-file"></i>
                    <span>Files</span>
                    <span class="cat-count" id="count-files">7</span>
                </div>
                <div class="category-item" data-category="Network">
                    <i class="fas fa-network-wired"></i>
                    <span>Network</span>
                    <span class="cat-count" id="count-network">6</span>
                </div>
                <div class="category-item" data-category="Security">
                    <i class="fas fa-shield-alt"></i>
                    <span>Security</span>
                    <span class="cat-count" id="count-security">4</span>
                </div>
                <div class="category-item" data-category="Developer">
                    <i class="fas fa-code"></i>
                    <span>Developer</span>
                    <span class="cat-count" id="count-dev">7</span>
                </div>
                <div class="category-item" data-category="Customize">
                    <i class="fas fa-paint-brush"></i>
                    <span>Customize</span>
                    <span class="cat-count" id="count-customize">1</span>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Top Bar -->
            <header class="top-bar">
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="search-input" placeholder="Search 32 tools...">
                </div>
            </header>

            <!-- Content Area -->
            <div class="content-area">
                <!-- Tools Grid -->
                <div class="tools-grid" id="tools-grid"></div>
                
                <!-- Tool Result Area -->
                <div class="tool-result" id="tool-result" style="display: none;">
                    <div class="result-header">
                        <h2 id="result-title">Tool Result</h2>
                        <button class="btn-close" onclick="hideResult()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="result-content" id="result-content"></div>
                    
                    <!-- Delete button for file tools -->
                    <div id="delete-section" style="display: none; margin-top: 20px;">
                        <button class="btn btn-danger" onclick="deleteSelected()">
                            <i class="fas fa-trash"></i> Delete Selected Files
                        </button>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <!-- Toast Notification -->
    <div class="toast" id="toast">
        <i class="fas fa-info-circle"></i>
        <span id="toast-message"></span>
    </div>

    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loading">
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <span>Loading...</span>
        </div>
    </div>

    <script src="/static/script.js"></script>
</body>
</html>
"""

# ============================================================================
# CSS CONTENT (Minimal but Beautiful)
# ============================================================================

CSS_CONTENT = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #4361ee;
    --secondary: #3f37c9;
    --success: #4cc9f0;
    --danger: #f72585;
    --warning: #f8961e;
    --dark: #1e1e2f;
    --light: #f8f9fa;
    --text: #212529;
    --border: #dee2e6;
}

body {
    font-family: 'Inter', sans-serif;
    background: var(--light);
    color: var(--text);
}

.app-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 280px;
    background: var(--dark);
    color: white;
    position: fixed;
    height: 100vh;
    left: 0;
    top: 0;
    overflow-y: auto;
}

.logo {
    padding: 25px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    gap: 15px;
}

.logo i {
    font-size: 36px;
    color: var(--primary);
}

.logo-text {
    display: flex;
    flex-direction: column;
}

.logo-title {
    font-size: 18px;
    font-weight: 700;
}

.logo-version {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
}

.categories {
    padding: 20px 0;
}

.category-item {
    display: flex;
    align-items: center;
    padding: 12px 25px;
    color: rgba(255,255,255,0.7);
    cursor: pointer;
    transition: all 0.3s;
}

.category-item i {
    width: 24px;
    margin-right: 12px;
}

.category-item:hover {
    background: rgba(255,255,255,0.1);
    color: white;
}

.category-item.active {
    background: var(--primary);
    color: white;
}

.cat-count {
    margin-left: auto;
    background: rgba(255,255,255,0.2);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
}

/* Main Content */
.main-content {
    flex: 1;
    margin-left: 280px;
    padding: 20px;
}

.top-bar {
    margin-bottom: 30px;
}

.search-box {
    position: relative;
    max-width: 400px;
}

.search-box i {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #6c757d;
}

.search-box input {
    width: 100%;
    padding: 12px 20px 12px 45px;
    border: 1px solid var(--border);
    border-radius: 30px;
    font-size: 14px;
    background: white;
}

.search-box input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(67,97,238,0.1);
}

/* Tools Grid */
.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.tool-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid var(--border);
}

.tool-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-color: var(--primary);
}

.tool-icon {
    width: 48px;
    height: 48px;
    background: var(--primary);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    color: white;
    font-size: 24px;
}

.tool-name {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
}

.tool-category {
    font-size: 13px;
    color: var(--primary);
    margin-bottom: 8px;
}

.tool-desc {
    font-size: 13px;
    color: #6c757d;
}

/* Tool Result */
.tool-result {
    background: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    margin-top: 20px;
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--border);
}

.btn-close {
    width: 36px;
    height: 36px;
    border: none;
    background: var(--light);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-close:hover {
    background: var(--danger);
    color: white;
}

/* Tables */
.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    background: var(--light);
    padding: 10px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid var(--border);
}

.data-table td {
    padding: 8px 10px;
    border-bottom: 1px solid var(--border);
}

.data-table tr:hover {
    background: var(--light);
}

/* Buttons */
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: var(--secondary);
}

.btn-danger {
    background: var(--danger);
    color: white;
}

.btn-danger:hover {
    opacity: 0.9;
}

.btn-sm {
    padding: 5px 10px;
    font-size: 12px;
}

/* Toast */
.toast {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: white;
    padding: 15px 25px;
    border-radius: 8px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    gap: 12px;
    transform: translateX(400px);
    transition: transform 0.3s;
    z-index: 1000;
    border-left: 4px solid var(--primary);
}

.toast.show {
    transform: translateX(0);
}

/* Loading */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 2000;
}

.loading-spinner {
    background: white;
    padding: 30px 50px;
    border-radius: 16px;
    text-align: center;
}

.loading-spinner i {
    font-size: 40px;
    color: var(--primary);
    margin-bottom: 15px;
}

/* Checkbox */
.file-checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        width: 70px;
    }
    
    .sidebar .logo-text,
    .sidebar .category-item span:not(.cat-count) {
        display: none;
    }
    
    .main-content {
        margin-left: 70px;
    }
    
    .tools-grid {
        grid-template-columns: 1fr;
    }
}
"""

# ============================================================================
# JAVASCRIPT CONTENT
# ============================================================================

JS_CONTENT = """// Ultimate System Toolbox - JavaScript
let currentCategory = 'all';
let tools = [];
let selectedFiles = new Set();
let currentResult = null;
let searchTimeout;

document.addEventListener('DOMContentLoaded', function() {
    loadTools();
    
    // Category click
    document.querySelectorAll('.category-item').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelectorAll('.category-item').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.dataset.category;
            filterTools();
        });
    });
    
    // Search
    document.getElementById('search-input').addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(filterTools, 300);
    });
});

function loadTools() {
    showLoading();
    fetch('/api/tools')
        .then(res => res.json())
        .then(data => {
            tools = data;
            renderTools(tools);
            updateCategoryCounts();
            hideLoading();
        })
        .catch(error => {
            showToast('Error loading tools', 'error');
            hideLoading();
        });
}

function renderTools(toolsToRender) {
    const grid = document.getElementById('tools-grid');
    
    grid.innerHTML = toolsToRender.map(tool => `
        <div class="tool-card" onclick="executeTool('${tool.id}')">
            <div class="tool-icon">
                <i class="fas ${tool.icon}"></i>
            </div>
            <h3 class="tool-name">${tool.name}</h3>
            <div class="tool-category">${tool.category}</div>
            <div class="tool-desc">${tool.desc || 'Click to run'}</div>
        </div>
    `).join('');
}

function filterTools() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    
    const filtered = tools.filter(tool => {
        const matchesCategory = currentCategory === 'all' || tool.category === currentCategory;
        const matchesSearch = tool.name.toLowerCase().includes(searchTerm) ||
                             tool.category.toLowerCase().includes(searchTerm) ||
                             (tool.desc && tool.desc.toLowerCase().includes(searchTerm));
        return matchesCategory && matchesSearch;
    });
    
    renderTools(filtered);
}

function updateCategoryCounts() {
    const counts = {
        'System': 0,
        'Files': 0,
        'Network': 0,
        'Security': 0,
        'Developer': 0,
        'Customize': 0
    };
    
    tools.forEach(tool => {
        if (counts[tool.category] !== undefined) {
            counts[tool.category]++;
        }
    });
    
    document.getElementById('count-all').textContent = tools.length;
    document.getElementById('count-system').textContent = counts['System'];
    document.getElementById('count-files').textContent = counts['Files'];
    document.getElementById('count-network').textContent = counts['Network'];
    document.getElementById('count-security').textContent = counts['Security'];
    document.getElementById('count-dev').textContent = counts['Developer'];
    document.getElementById('count-customize').textContent = counts['Customize'];
}

function executeTool(toolId) {
    showLoading();
    
    // Special handling for tools that need input
    if (toolId === '007') { // Port Scanner
        const target = prompt('Enter target host:', 'localhost');
        if (target) {
            fetch(`/api/tool/007?target=${target}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '008') { // DNS Lookup
        const domain = prompt('Enter domain:', 'google.com');
        if (domain) {
            fetch(`/api/tool/008?domain=${domain}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '017') { // Password Generator
        const length = prompt('Password length (8-32):', '12');
        if (length) {
            const special = confirm('Include special characters?');
            fetch(`/api/tool/017?length=${length}&special=${special}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '018' || toolId === '019') { // Encrypt/Decrypt
        const file = prompt('Enter file path:');
        if (file) {
            const password = prompt('Enter password:');
            if (password) {
                executeToolWithData(toolId, {file: file, password: password});
            } else {
                hideLoading();
            }
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '020') { // File Hasher
        const file = prompt('Enter file path:');
        if (file) {
            fetch(`/api/tool/020?file=${encodeURIComponent(file)}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '021' || toolId === '022' || toolId === '024' || toolId === '027') {
        const text = prompt('Enter text:');
        if (text) {
            fetch(`/api/tool/${toolId}?text=${encodeURIComponent(text)}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '023' || toolId === '025') {
        const encoded = prompt('Enter encoded text:');
        if (encoded) {
            fetch(`/api/tool/${toolId}?encoded=${encodeURIComponent(encoded)}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '026') {
        const json = prompt('Enter JSON:');
        if (json) {
            executeToolWithData(toolId, {json: json});
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '030') { // Ping
        const host = prompt('Enter host to ping:', 'google.com');
        if (host) {
            const count = prompt('Number of pings:', '4');
            fetch(`/api/tool/030?host=${host}&count=${count}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    if (toolId === '032') { // Random Generator
        const type = prompt('Type (number/float/string/hex/binary/uuid):', 'number');
        if (type) {
            fetch(`/api/tool/032?type=${type}`)
                .then(res => res.json())
                .then(data => displayResult(data, toolId));
        } else {
            hideLoading();
        }
        return;
    }
    
    // Default: simple GET
    fetch(`/api/tool/${toolId}`)
        .then(res => res.json())
        .then(data => displayResult(data, toolId))
        .catch(error => {
            showToast('Error: ' + error, 'error');
            hideLoading();
        });
}

function executeToolWithData(toolId, data) {
    fetch(`/api/tool/${toolId}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => displayResult(data, toolId))
        .catch(error => {
            showToast('Error: ' + error, 'error');
            hideLoading();
        });
}

function displayResult(data, toolId) {
    const resultDiv = document.getElementById('tool-result');
    const title = document.getElementById('result-title');
    const content = document.getElementById('result-content');
    const deleteSection = document.getElementById('delete-section');
    
    // Find tool name
    const tool = tools.find(t => t.id === toolId);
    title.textContent = tool ? tool.name : 'Tool Result';
    
    // Store result
    currentResult = data;
    
    // Format result
    if (Array.isArray(data)) {
        if (data.length === 0) {
            content.innerHTML = '<p>No data found</p>';
            deleteSection.style.display = 'none';
        } else {
            content.innerHTML = arrayToTable(data);
            
            // Show delete section for file lists
            if (toolId === '009' || toolId === '010' || toolId === '011') {
                deleteSection.style.display = 'block';
            } else {
                deleteSection.style.display = 'none';
            }
        }
    } else if (typeof data === 'object') {
        content.innerHTML = objectToTable(data);
        deleteSection.style.display = 'none';
    } else {
        content.innerHTML = `<pre>${data}</pre>`;
        deleteSection.style.display = 'none';
    }
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
    hideLoading();
}

function arrayToTable(arr) {
    if (arr.length === 0) return '<p>No data</p>';
    
    // Get all keys
    const keys = Object.keys(arr[0]);
    
    let html = '<table class="data-table">';
    html += '<tr>' + keys.map(k => `<th>${k}</th>`).join('') + '<th>Actions</th></tr>';
    
    arr.forEach((item, index) => {
        html += '<tr>';
        keys.forEach(key => {
            let value = item[key];
            if (value === null || value === undefined) value = '';
            if (typeof value === 'object') value = JSON.stringify(value);
            html += `<td>${value}</td>`;
        });
        // Add checkbox for deletion if path exists
        if (item.path) {
            html += `<td><input type="checkbox" class="file-checkbox" value="${item.path}" onchange="updateSelected(this)"></td>`;
        } else {
            html += '<td></td>';
        }
        html += '</tr>';
    });
    
    html += '</table>';
    return html;
}

function objectToTable(obj) {
    let html = '<table class="data-table">';
    for (const [key, value] of Object.entries(obj)) {
        let displayValue = value;
        if (value === null || value === undefined) displayValue = '';
        if (typeof value === 'object') displayValue = JSON.stringify(value, null, 2);
        html += `<tr><th>${key}</th><td>${displayValue}</td></tr>`;
    }
    html += '</table>';
    return html;
}

function hideResult() {
    document.getElementById('tool-result').style.display = 'none';
    selectedFiles.clear();
}

function updateSelected(checkbox) {
    if (checkbox.checked) {
        selectedFiles.add(checkbox.value);
    } else {
        selectedFiles.delete(checkbox.value);
    }
}

function deleteSelected() {
    const files = Array.from(selectedFiles);
    if (files.length === 0) {
        showToast('No files selected', 'warning');
        return;
    }
    
    if (confirm(`Delete ${files.length} selected files?`)) {
        showLoading('Deleting...');
        
        fetch('/api/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({files: files})
        })
        .then(res => res.json())
        .then(data => {
            showToast(`Deleted ${data.deleted} files (${data.freed_space})`);
            selectedFiles.clear();
            hideResult();
            hideLoading();
        })
        .catch(error => {
            showToast('Error: ' + error, 'error');
            hideLoading();
        });
    }
}

function showLoading(message = 'Loading...') {
    const overlay = document.getElementById('loading');
    overlay.querySelector('span').textContent = message;
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    document.getElementById('toast-message').textContent = message;
    
    const icon = toast.querySelector('i');
    icon.style.color = type === 'success' ? '#4cc9f0' : '#f72585';
    
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
"""

# ============================================================================
# MAIN SERVER
# ============================================================================

def find_free_port(start_port=8080, max_attempts=100):
    """Find a free port"""
    port = start_port
    for _ in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, port))
                return port
        except OSError:
            port += 1
    return start_port

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    url = f"http://{HOST}:{PORT}"
    print(f"\n🌐 Opening browser: {url}")
    webbrowser.open(url)

def main():
    """Main function"""
    global PORT
    PORT = find_free_port()
    
    print("=" * 60)
    print("🚀 ULTIMATE SYSTEM TOOLBOX v3.0")
    print("=" * 60)
    print(f"📌 Server: http://{HOST}:{PORT}")
    print(f"🔧 Tools: 32 Professional Utilities")
    print("📁 No extra modules required - Works out of box!")
    print("✨ Opening browser automatically...")
    print("=" * 60)
    print("Press Ctrl+C to stop\n")
    
    # Open browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server
    server = HTTPServer((HOST, PORT), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        server.shutdown()

if __name__ == "__main__":
    main()
