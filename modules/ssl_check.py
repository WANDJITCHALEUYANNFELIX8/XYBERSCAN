import ssl
import socket
import datetime

def check_ssl(url):
    
    results = {
        "url": url,
        "ssl_valid": None,
        "expiry_date": None,
        "days_remaining": None,
        "issuer": None,
        "tls_version": None,
        "expired": None,
        "errors": []
    }
    
    try:
        #extraction du domaine depuis l'URL#
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        
        #Créer un contexte SSL sécurisé#
        context = ssl.create_default_context()
        
        # Connexion au serveur sur le port 443
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                
                # Récupérer le certificat
                cert = ssock.getpeercert()
                
                # Version TLS utilisée
                results["version_tls"] = ssock.version()
                
                # Date d'expiration
                expiry_str = cert["pas apres"]
                expiry_date = datetime.datetime.strptime(
                    expiry_str, "%b %d %H:%M:%S %Y %Z"
                )
                results["date_d'expiration"] = str(expiry_date)
                
                # Jours restants avant expiration
                now = datetime.datetime.utcnow()
                delta = expiry_date - now
                results["jours_restant"] = delta.days
                results["expire"] = delta.days < 0
                
                # Émetteur du certificat
                issuer = dict(x[0] for x in cert["issuer"])
                results["issuer"] = issuer.get(
                    "organizationName", "Inconnu"
                )
                
                results["ssl_valid"] = True
                
    except ssl.SSLCertVerificationError:
        results["ssl_valid"] = False
        results["errors"].append("Certificat invalide ou non approuvé")
        
    except ssl.SSLError as e:
        results["ssl_valid"] = False
        results["errors"].append(f"Erreur SSL : {str(e)}")
        
    except socket.timeout:
        results["errors"].append("Timeout — serveur inaccessible")
        
    except Exception as e:
        results["errors"].append(f"Erreur : {str(e)}")
    
    return results

