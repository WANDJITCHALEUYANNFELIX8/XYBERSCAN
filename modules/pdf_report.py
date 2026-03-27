from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

# ─── PALETTE DE COULEURS ───
DARK_BG     = colors.HexColor("#0D1117")
CYAN        = colors.HexColor("#00B4D8")
GREEN       = colors.HexColor("#2ECC71")
RED         = colors.HexColor("#E74C3C")
YELLOW      = colors.HexColor("#F39C12")
BLUE        = colors.HexColor("#2E75B6")
LIGHT_GRAY  = colors.HexColor("#F5F8FC")
DARK_GRAY   = colors.HexColor("#2C3E50")
WHITE       = colors.white
MID_GRAY    = colors.HexColor("#95A5A6")
CARD_BG     = colors.HexColor("#EBF5FB")
RED_BG      = colors.HexColor("#FADBD8")
GREEN_BG    = colors.HexColor("#D5F5E3")
YELLOW_BG   = colors.HexColor("#FDEBD0")

def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="MainTitle",
        fontName="Helvetica-Bold",
        fontSize=28,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="SubTitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=CYAN,
        alignment=TA_CENTER,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=4
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=4,
        leading=14
    ))
    styles.add(ParagraphStyle(
        name="BodyBold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="Small",
        fontName="Helvetica",
        fontSize=8,
        textColor=MID_GRAY,
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="RecoTitle",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK_GRAY,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="RecoBody",
        fontName="Helvetica",
        fontSize=9,
        textColor=DARK_GRAY,
        spaceAfter=3,
        leading=13,
        leftIndent=10
    ))
    return styles


def section_header(title, color=BLUE):
    """Crée un bloc titre de section coloré."""
    data = [[Paragraph(f"<b>{title}</b>",
             ParagraphStyle("sh", fontName="Helvetica-Bold",
                            fontSize=13, textColor=WHITE))]]
    t = Table(data, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t


def status_row(label, value, status="ok"):
    """Ligne avec icône colorée."""
    if status == "ok":
        icon  = "✓"
        color = GREEN
        bg    = GREEN_BG
    elif status == "warning":
        icon  = "!"
        color = YELLOW
        bg    = YELLOW_BG
    else:
        icon  = "✗"
        color = RED
        bg    = RED_BG

    icon_style  = ParagraphStyle("i", fontName="Helvetica-Bold",
                                 fontSize=11, textColor=color, alignment=TA_CENTER)
    label_style = ParagraphStyle("l", fontName="Helvetica-Bold",
                                 fontSize=9,  textColor=DARK_GRAY)
    value_style = ParagraphStyle("v", fontName="Helvetica",
                                 fontSize=9,  textColor=DARK_GRAY)

    data = [[
        Paragraph(icon,  icon_style),
        Paragraph(label, label_style),
        Paragraph(str(value), value_style)
    ]]
    t = Table(data, colWidths=[1*cm, 6*cm, 10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("ROUNDEDCORNERS", [4]),
        ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.white),
    ]))
    return t


def reco_box(title, items, color=BLUE, bg=CARD_BG):
    """Boîte de recommandations."""
    style_title = ParagraphStyle("rt", fontName="Helvetica-Bold",
                                 fontSize=10, textColor=WHITE)
    style_item  = ParagraphStyle("ri", fontName="Helvetica",
                                 fontSize=9,  textColor=DARK_GRAY, leading=13)

    content = [Paragraph(f"  {title}", style_title)]
    rows = [[content[0]]]
    t_header = Table(rows, colWidths=[17*cm])
    t_header.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), color),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))

    body_rows = [[Paragraph(f"  • {item}", style_item)] for item in items]
    t_body = Table(body_rows, colWidths=[17*cm])
    t_body.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
    ]))
    return [t_header, t_body]


def score_bar(score):
    """Barre de score visuelle."""
    if score >= 80:
        color  = GREEN
        niveau = "BON"
        emoji  = "🟢"
    elif score >= 50:
        color  = YELLOW
        niveau = "MOYEN"
        emoji  = "🟡"
    else:
        color  = RED
        niveau = "FAIBLE"
        emoji  = "🔴"

    # Barre
    filled  = int(score / 5)
    empty   = 20 - filled
    bar_str = "█" * filled + "░" * empty

    score_style = ParagraphStyle("sc", fontName="Helvetica-Bold",
                                 fontSize=22, textColor=color, alignment=TA_CENTER)
    bar_style   = ParagraphStyle("ba", fontName="Helvetica",
                                 fontSize=14, textColor=color, alignment=TA_CENTER)
    niv_style   = ParagraphStyle("nv", fontName="Helvetica-Bold",
                                 fontSize=14, textColor=color, alignment=TA_CENTER)

    data = [[
        Paragraph(f"{score}/100", score_style),
        Paragraph(bar_str, bar_style),
        Paragraph(f"{niveau}", niv_style),
    ]]
    t = Table(data, colWidths=[4*cm, 9*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_GRAY),
        ("TOPPADDING",    (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS", [8]),
        ("BOX", (0,0), (-1,-1), 2, color),
    ]))
    return t


def generate_pdf_report(
    url,
    headers_result=None,
    ssl_result=None,
    sensitive_result=None,
    ports_result=None,
    output_path="xyberscan_report.pdf"
):
    styles = get_styles()
    story  = []

    # ═══════════════════════════════
    # PAGE DE COUVERTURE
    # ═══════════════════════════════
    cover_data = [[
        Paragraph("XYBERSCAN", styles["MainTitle"]),
    ]]
    cover = Table(cover_data, colWidths=[17*cm])
    cover.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 30),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [10]),
    ]))
    story.append(cover)

    sub_data = [[Paragraph("Rapport d'analyse de vulnérabilités web", styles["SubTitle"])]]
    sub = Table(sub_data, colWidths=[17*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS", [10]),
    ]))
    story.append(sub)
    story.append(Spacer(1, 0.5*cm))

    # Infos cible
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    info_data = [
        [Paragraph("<b>Cible analysée</b>", styles["BodyBold"]),
         Paragraph(url, styles["Body"])],
        [Paragraph("<b>Date du rapport</b>", styles["BodyBold"]),
         Paragraph(date_str, styles["Body"])],
        [Paragraph("<b>Outil</b>", styles["BodyBold"]),
         Paragraph("XyberScan v1.0 — Communauté Xyberclan", styles["Body"])],
    ]
    info_table = Table(info_data, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), LIGHT_GRAY),
        ("BACKGROUND",    (1,0), (1,-1), WHITE),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("LINEBELOW",     (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
        ("BOX",           (0,0), (-1,-1), 1, BLUE),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.8*cm))

    # Score global
    score = _calculate_score(headers_result, ssl_result, sensitive_result, ports_result)
    story.append(section_header("SCORE DE SÉCURITÉ GLOBAL", DARK_GRAY))
    story.append(Spacer(1, 0.3*cm))
    story.append(score_bar(score))
    story.append(Spacer(1, 0.5*cm))

    story.append(PageBreak())

    # ═══════════════════════════════
    # SECTION HEADERS
    # ═══════════════════════════════
    if headers_result and "error" not in headers_result:
        story.append(section_header("1 — HEADERS DE SÉCURITÉ HTTP", BLUE))
        story.append(Spacer(1, 0.3*cm))

        for h in headers_result.get("present", []):
            story.append(status_row(h, "Présent et actif", "ok"))

        for h in headers_result.get("missing", []):
            story.append(status_row(h, "Header manquant", "error"))

        for h in headers_result.get("misconfigured", []):
            story.append(status_row(h, "Mal configuré", "warning"))

        if headers_result.get("http_to_https"):
            story.append(status_row("Redirection HTTP → HTTPS", "Active", "ok"))
        else:
            story.append(status_row("Redirection HTTP → HTTPS", "Inactive", "error"))

        # Recommandations headers
        recos = []
        if "Content-Security-Policy" in headers_result.get("missing", []):
            recos.append("Ajouter le header Content-Security-Policy pour bloquer les attaques XSS")
        if "X-Frame-Options" in headers_result.get("missing", []):
            recos.append("Ajouter X-Frame-Options: DENY pour prévenir le clickjacking")
        if "Strict-Transport-Security" in headers_result.get("missing", []):
            recos.append("Activer HSTS pour forcer les connexions HTTPS")
        if "X-Content-Type-Options" in headers_result.get("missing", []):
            recos.append("Ajouter X-Content-Type-Options: nosniff")
        if not headers_result.get("http_to_https"):
            recos.append("Configurer une redirection permanente 301 de HTTP vers HTTPS")

        if recos:
            story.append(Spacer(1, 0.4*cm))
            for elem in reco_box("ACTIONS RECOMMANDÉES", recos, RED, RED_BG):
                story.append(elem)

        story.append(Spacer(1, 0.6*cm))

    # ═══════════════════════════════
    # SECTION SSL
    # ═══════════════════════════════
    if ssl_result and "error" not in ssl_result:
        story.append(section_header("2 — CERTIFICAT SSL / TLS", BLUE))
        story.append(Spacer(1, 0.3*cm))

        # Validité
        if ssl_result.get("ssl_valid"):
            story.append(status_row("Certificat SSL", "Valide", "ok"))
        else:
            story.append(status_row("Certificat SSL", "Invalide ou non approuvé", "error"))

        # Version TLS
        tls = ssl_result.get("tls_version", "Inconnu")
        if tls in ["TLSv1.2", "TLSv1.3"]:
            story.append(status_row("Version TLS", tls, "ok"))
        else:
            story.append(status_row("Version TLS", f"{tls} — obsolète !", "error"))

        # Expiration
        days = ssl_result.get("days_remaining")
        if days is not None:
            if days > 30:
                story.append(status_row("Expiration", f"Dans {days} jours", "ok"))
            elif days > 0:
                story.append(status_row("Expiration", f"Dans {days} jours — renouveler bientôt !", "warning"))
            else:
                story.append(status_row("Expiration", "Certificat EXPIRÉ !", "error"))

        # Émetteur
        issuer = ssl_result.get("issuer", "Inconnu")
        story.append(status_row("Émetteur", issuer, "ok"))

        # Recommandations SSL
        recos_ssl = []
        if not ssl_result.get("ssl_valid"):
            recos_ssl.append("Installer un certificat SSL valide (Let's Encrypt est gratuit)")
        if tls not in ["TLSv1.2", "TLSv1.3"]:
            recos_ssl.append("Désactiver TLS 1.0 et 1.1 sur le serveur — utiliser TLS 1.2 minimum")
        if days is not None and 0 < days <= 30:
            recos_ssl.append(f"Renouveler le certificat SSL — expire dans {days} jours")
        if days is not None and days <= 0:
            recos_ssl.append("URGENT : Renouveler immédiatement le certificat SSL expiré")

        if recos_ssl:
            story.append(Spacer(1, 0.4*cm))
            for elem in reco_box("ACTIONS RECOMMANDÉES", recos_ssl, RED, RED_BG):
                story.append(elem)

        story.append(Spacer(1, 0.6*cm))

    # ═══════════════════════════════
    # SECTION PAGES SENSIBLES
    # ═══════════════════════════════
    if sensitive_result:
        story.append(section_header("3 — PAGES SENSIBLES EXPOSÉES", BLUE))
        story.append(Spacer(1, 0.3*cm))

        found     = sensitive_result.get("found", [])
        forbidden = sensitive_result.get("forbidden", [])
        total     = sensitive_result.get("total_tested", 0)

        story.append(status_row("Pages testées", f"{total} URLs analysées", "ok"))

        if found:
            for p in found:
                story.append(status_row(
                    f"Page accessible : {p['page']}",
                    "Accessible publiquement — CRITIQUE",
                    "error"
                ))
        else:
            story.append(status_row("Pages sensibles", "Aucune page sensible accessible", "ok"))

        if forbidden:
            for p in forbidden:
                story.append(status_row(
                    f"Page protégée : {p['page']}",
                    "Existe mais accès refusé (403)",
                    "warning"
                ))

        # Recommandations pages sensibles
        recos_pages = []
        if found:
            recos_pages.append("Restreindre l'accès aux pages sensibles via .htaccess ou la config du serveur")
            recos_pages.append("Supprimer les fichiers de backup et de configuration exposés")
            recos_pages.append("Ne jamais laisser .env, .git ou config.php accessibles publiquement")
            recos_pages.append("Configurer un pare-feu applicatif (WAF) pour bloquer ces accès")
        if forbidden:
            recos_pages.append("Les pages en 403 existent — vérifier qu'elles ne peuvent pas être contournées")

        if recos_pages:
            story.append(Spacer(1, 0.4*cm))
            for elem in reco_box("ACTIONS RECOMMANDÉES", recos_pages, RED, RED_BG):
                story.append(elem)

        story.append(Spacer(1, 0.6*cm))

    # ═══════════════════════════════
    # SECTION PORTS
    # ═══════════════════════════════
    if ports_result and not ports_result.get("errors"):
        story.append(section_header("4 — SCAN DE PORTS", BLUE))
        story.append(Spacer(1, 0.3*cm))

        open_ports = ports_result.get("open_ports", [])
        dangerous  = ports_result.get("dangerous_open", [])
        duration   = ports_result.get("scan_duration", "")
        host       = ports_result.get("host", "")

        story.append(status_row("Hôte scanné", host, "ok"))
        story.append(status_row("Durée du scan", duration, "ok"))
        story.append(status_row("Ports ouverts détectés", str(len(open_ports)), "ok" if not dangerous else "warning"))

        if open_ports:
            story.append(Spacer(1, 0.3*cm))
            # Tableau des ports
            port_header = [
                Paragraph("<b>Port</b>",    ParagraphStyle("ph", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)),
                Paragraph("<b>Service</b>", ParagraphStyle("ph", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)),
                Paragraph("<b>Statut</b>",  ParagraphStyle("ph", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)),
                Paragraph("<b>Niveau</b>",  ParagraphStyle("ph", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)),
            ]
            port_rows = [port_header]

            ps = ParagraphStyle("pc", fontName="Helvetica", fontSize=9, textColor=DARK_GRAY)
            for p in sorted(open_ports, key=lambda x: x["port"]):
                niv_color = RED if p["niveau"] == "CRITIQUE" else GREEN
                niv_style = ParagraphStyle("pn", fontName="Helvetica-Bold", fontSize=9, textColor=niv_color)
                port_rows.append([
                    Paragraph(str(p["port"]), ps),
                    Paragraph(p["service"],   ps),
                    Paragraph("OUVERT",       ps),
                    Paragraph(p["niveau"],    niv_style),
                ])

            t_ports = Table(port_rows, colWidths=[3*cm, 6*cm, 4*cm, 4*cm])
            t_ports.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,0),  DARK_GRAY),
                ("BACKGROUND",    (0,1), (-1,-1), WHITE),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
            ]))
            story.append(t_ports)

        # Recommandations ports
        recos_ports = []
        if dangerous:
            for p in dangerous:
                if p["port"] == 21:
                    recos_ports.append("Port 21 (FTP) ouvert — Désactiver FTP, utiliser SFTP à la place")
                if p["port"] == 23:
                    recos_ports.append("Port 23 (Telnet) ouvert — Désactiver Telnet immédiatement, utiliser SSH")
                if p["port"] == 445:
                    recos_ports.append("Port 445 (SMB) ouvert — Fermer si non nécessaire, vecteur de ransomware")
                if p["port"] == 3389:
                    recos_ports.append("Port 3389 (RDP) ouvert — Restreindre l'accès par IP, activer NLA")
                if p["port"] == 6379:
                    recos_ports.append("Port 6379 (Redis) ouvert — Redis ne doit jamais être exposé publiquement")
                if p["port"] == 27017:
                    recos_ports.append("Port 27017 (MongoDB) ouvert — Sécuriser MongoDB avec authentification")

        if recos_ports:
            story.append(Spacer(1, 0.4*cm))
            for elem in reco_box("ACTIONS RECOMMANDÉES — PORTS DANGEREUX", recos_ports, RED, RED_BG):
                story.append(elem)

        story.append(Spacer(1, 0.6*cm))

    # ═══════════════════════════════
    # RÉSUMÉ FINAL
    # ═══════════════════════════════
    story.append(PageBreak())
    story.append(section_header("RÉSUMÉ ET PLAN D'ACTION", DARK_GRAY))
    story.append(Spacer(1, 0.4*cm))
    story.append(score_bar(score))
    story.append(Spacer(1, 0.5*cm))

    # Plan d'action par priorité
    critiques  = []
    moyens     = []
    faibles    = []

    if headers_result:
        for h in headers_result.get("missing", []):
            critiques.append(f"Ajouter le header manquant : {h}")
        if not headers_result.get("http_to_https"):
            critiques.append("Activer la redirection HTTP → HTTPS")

    if ssl_result:
        if not ssl_result.get("ssl_valid"):
            critiques.append("Installer un certificat SSL valide immédiatement")
        days = ssl_result.get("days_remaining")
        if days is not None and days <= 0:
            critiques.append("URGENT : Renouveler le certificat SSL expiré")
        elif days is not None and days <= 30:
            moyens.append(f"Renouveler le certificat SSL (expire dans {days} jours)")

    if sensitive_result:
        for p in sensitive_result.get("found", []):
            critiques.append(f"Bloquer l'accès à la page sensible : {p['page']}")

    if ports_result:
        for p in ports_result.get("dangerous_open", []):
            critiques.append(f"Fermer le port dangereux : {p['port']} ({p['service']})")

    if critiques:
        for elem in reco_box("PRIORITÉ HAUTE — À corriger immédiatement", critiques, RED, RED_BG):
            story.append(elem)
        story.append(Spacer(1, 0.3*cm))

    if moyens:
        for elem in reco_box("PRIORITÉ MOYENNE — À corriger sous 30 jours", moyens, YELLOW, YELLOW_BG):
            story.append(elem)
        story.append(Spacer(1, 0.3*cm))

    if not critiques and not moyens:
        for elem in reco_box("EXCELLENT — Aucun problème critique détecté",
                             ["Continuer à surveiller régulièrement votre sécurité",
                              "Mettre à jour régulièrement vos dépendances",
                              "Effectuer des audits de sécurité périodiques"],
                             GREEN, GREEN_BG):
            story.append(elem)

    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    story.append(Spacer(1, 0.2*cm))

    footer_style = ParagraphStyle("ft", fontName="Helvetica",
                                  fontSize=8, textColor=MID_GRAY, alignment=TA_CENTER)
    story.append(Paragraph(
        f"Rapport généré par XyberScan v1.0 — Xyberclan | {date_str}",
        footer_style
    ))
    story.append(Paragraph(
        "Ce rapport est fourni à titre informatif. Xyberclan décline toute responsabilité pour toute utilisation non autorisée.",
        footer_style
    ))

    # ─── BUILD PDF ───
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    doc.build(story)
    print(f"\n[✓] Rapport PDF généré : {output_path}")
    return output_path


def _calculate_score(headers_result, ssl_result, sensitive_result, ports_result=None):
    score = 100

    if headers_result and "missing" in headers_result:
        score -= len(headers_result["missing"]) * 8
    if headers_result and "misconfigured" in headers_result:
        score -= len(headers_result["misconfigured"]) * 5

    if ssl_result:
        if not ssl_result.get("ssl_valid"):
            score -= 30
        if ssl_result.get("expired"):
            score -= 20
        tls = ssl_result.get("tls_version", "")
        if tls not in ["TLSv1.2", "TLSv1.3"]:
            score -= 15

    if sensitive_result:
        score -= len(sensitive_result.get("found", [])) * 10

    if ports_result:
        score -= len(ports_result.get("dangerous_open", [])) * 10
        score -= len(ports_result.get("open_ports", [])) * 2

    return max(0, score)


# ─── TEST DIRECT ───
if __name__ == "__main__":
    # Données de test simulées
    test_ssl = {
        "ssl_valid": True,
        "tls_version": "TLSv1.3",
        "days_remaining": 45,
        "issuer": "Let's Encrypt",
        "expired": False
    }
    test_headers = {
        "present": ["X-Content-Type-Options", "Referrer-Policy"],
        "missing": ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security"],
        "misconfigured": [],
        "http_to_https": True
    }
    test_sensitive = {
        "found": [{"page": "/.env"}, {"page": "/admin"}],
        "forbidden": [{"page": "/phpmyadmin"}],
        "total_tested": 30
    }
    test_ports = {
        "host": "xyberclan.dev",
        "open_ports": [
            {"port": 80,  "service": "HTTP",  "status": "OUVERT", "niveau": "INFO"},
            {"port": 443, "service": "HTTPS", "status": "OUVERT", "niveau": "INFO"},
            {"port": 22,  "service": "SSH",   "status": "OUVERT", "niveau": "INFO"},
            {"port": 6379,"service": "Redis", "status": "OUVERT", "niveau": "CRITIQUE"},
        ],
        "dangerous_open": [{"port": 6379, "service": "Redis", "niveau": "CRITIQUE"}],
        "scan_duration": "2.34s",
        "errors": []
    }

    generate_pdf_report(
        url="https://xyberclan.dev",
        headers_result=test_headers,
        ssl_result=test_ssl,
        sensitive_result=test_sensitive,
        ports_result=test_ports,
        output_path="/home/claude/xyberscan_report.pdf"
    )