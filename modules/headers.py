import requests
import json
from urllib.parse import urlparse#permettra l extraction du nom de domaine de l URL pour le test de HTTP



def analyze_headers(url):

	# Ajout automatique du schéma HTTPS si absent
	if not url.startswith(("http://", "https://")):
		url = "https://" + url
		
	results = {
		"initial_url": url,
		"final_url": None,
		"redirect_chain": [], 
		"present": [],
		"missing": [],
		"misconfigured": [],
		"server_info": None,
		"http_status": None,
		"http_redirect_to": None,
		"http_to_https": None,
		"hsts_present": None
	}
	
	
	print("================== Analyse des headers ====================\n\n")
	
	#on va analyser a la derniere redirection pour eviter fausses absences de certains headers l analyse de la premiere reponse du serveur n'est pas bonne car certains headers peuvent intervenir qu a certaines pages ou a la fin
	
	
	try:
	
		#extration du nom de domaine pour tester http
		parsed = urlparse(url)
		domain = parsed.netloc
		http_url=f"http://{domain}"
		
		#test si http repond sans redirection vers https
		try:
			#on ne suit pas la redirection pour avoir la premiere reponse du serveur http
			http_response = requests.get(http_url, timeout=5, allow_redirects =False)
			
			#verifie si http repond
			results["http_status"]=http_response.status_code
			
			#verifie si http rerdirige vers https
			if http_response.status_code in [301, 302, 307, 308]:
				
				location =http_response.headers.get("Location","")
				results["http_redirect_to"]=location
				
				if location.startswith("https://"):
					results["http_to_https"]=True
				else:
					results["http_to_https"]=False	 
				
			else:
				results["http_to_https"]=False
				
		except:
			results["http_status"] = "HTTP not accessible"
			results["http_to_https"] = False		
			
		#requete pour faire au serveur que ta requte provient d un vrai navigateur car plusieurs sites bloquent les scanners et donc on pourra avoir des faux headers
		
		headers_config = {
			"User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
		}
		
		
		#Autorise les redirections
		response = requests.get(url, timeout=5, allow_redirects =True, headers=headers_config)
		
		#URL finale après redirections
		results["final_url"] = response.url

		#Historique des redirections
		for resp in response.history:
			results["redirect_chain"].append({
				"status_code": resp.status_code,
				"redirect_to": resp.headers.get("Location")
			})
			print(resp.status_code, resp.url, resp.headers)
			
		#recupere la liste des headers
		headers=response.headers

		security_headers = {
			"Content-Security-Policy": "CSP", #contre xss
			"X-Frame-Options": "Clickjacking Protection",
			"Strict-Transport-Security": "HSTS",#force http à https
			"X-Content-Type-Options": "MIME Protection",
			"Referrer-Policy": "Referrer Control",
			"Permissions-Policy": "Browser Feature Control"
		}

		#verifie la presence de chacun header à un instant donne
		for header in security_headers:
			if header in headers :
				results["present"].append(header)
				
			else:
				results["missing"].append(header)
					
		
		#Analyse CSP		
		if "Content-Security-Policy" in headers:
			csp=headers["Content-Security-Policy"]
			if "unsafe-inline" in csp or "unsafe-eval" in csp:
				results["misconfigured"].append(" CSP contains unsafe directives")
				
		
		#Analyse HSTS
		if "Strict-Transport-Security" in headers:
			hsts = headers["Strict-Transport-Security"]
			if "max-age=0" in hsts:
				results["misconfigured"].append("HSTS max-age too low")
				
		#Analyse X-Frame-Options
		if "X-Frame-Options" in headers:
			if headers["X-Frame-Options"] not in ["DENY", "SAMEORIGIN"]:
				results["misconfigured"].append("X-Frame-Options weak")

		#Analyse serveur
		if "Server" in headers:
			results["server_info"]=headers["Server"]
		
			if "/" in results["server_info"] :
				results["misconfigured"].append("Server version exposed")
			
		# Vérifier HSTS sur réponse finale HTTPS
		if results["final_url"].startswith("https://"):
			if "Strict-Transport-Security" in headers:
				results["hsts_present"] = True
			else:
				results["hsts_present"] = False
				results["misconfigured"].append("HTTPS without HSTS")		
		else:
			results["hsts_present"]=False
		
				
		return results
	
	except Exception as e:
		return {"error": str(e)}	
		


