import socket
import concurrent.futures
from datetime import datetime

# Ports courants avec leur service associé
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB"
}

# Ports dangereux si ouverts
DANGEROUS_PORTS = [21, 23, 445, 3389, 6379, 27017]

def scan_port(host, port, timeout=1):
    """Teste si un port est ouvert sur le host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0  # True si ouvert
    except Exception:
        return port, False

def scan_ports(url):

    results = {
        "url": url,
        "host": None,
        "open_ports": [],
        "closed_ports": [],
        "dangerous_open": [],
        "scan_duration": None,
        "errors": []
    }

    try:
        # Extraire le domaine
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        results["host"] = domain

        # Résoudre l'IP
        host_ip = socket.gethostbyname(domain)

        print(f"\n[*] Scan de ports sur : {domain} ({host_ip})")
        print(f"[*] {len(COMMON_PORTS)} ports à scanner...\n")

        start_time = datetime.now()

        # Scan parallèle pour aller plus vite
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = {
                executor.submit(scan_port, host_ip, port): port
                for port in COMMON_PORTS
            }

            for future in concurrent.futures.as_completed(futures):
                port, is_open = future.result()
                service = COMMON_PORTS.get(port, "Inconnu")

                if is_open:
                    port_info = {
                        "port": port,
                        "service": service,
                        "status": "OUVERT",
                        "niveau": "CRITIQUE" if port in DANGEROUS_PORTS else "INFO"
                    }
                    results["open_ports"].append(port_info)
                    print(f"  [+] Port {port:5d} ({service:15s}) — OUVERT")

                    # Vérifier si dangereux
                    if port in DANGEROUS_PORTS:
                        results["dangerous_open"].append(port_info)
                        print(f"  [!] ATTENTION : Port {port} ({service}) dangereux !")
                else:
                    results["closed_ports"].append(port)

        # Durée du scan
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        results["scan_duration"] = f"{duration:.2f}s"

        print(f"\n[*] Scan terminé en {duration:.2f} secondes")
        print(f"[*] {len(results['open_ports'])} ports ouverts détectés")

        if results["dangerous_open"]:
            print(f"[!] {len(results['dangerous_open'])} ports dangereux ouverts !")

    except socket.gaierror:
        results["errors"].append("Impossible de résoudre le domaine")
    except Exception as e:
        results["errors"].append(f"Erreur : {str(e)}")

    return results


# Exécution directe pour test
if __name__ == "__main__":
    url = input("Entrez l'URL à scanner : ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    import json
    result = scan_ports(url)
    print("\n================== Résultat JSON ====================\n")
    print(json.dumps(result, indent=4))

