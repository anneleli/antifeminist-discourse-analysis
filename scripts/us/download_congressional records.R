library(jsonlite)
library(httr)

# API-Key für congress.gov 
api_key <- "EIGNER_API_KEY"

# Zielordner für Downloads
pfad <- "~/Desktop/Congress_Downloads"
dir.create(pfad, showWarnings = FALSE)
setwd(pfad)

# Hauptanfrage an die API: Liste aller verfügbaren Sitzungstage abrufen
# Limit auf 250 Einträge (Maximum der API) gesetzt
url_haupt <- paste0("https://api.congress.gov/v3/daily-congressional-record?
format=json&offset=0&limit=250&api_key=", api_key)
haupt_daten <- fromJSON(content(GET(url_haupt), "text", encoding = "UTF-8"))
records <- haupt_daten$dailyCongressionalRecord

# Schleife über alle verfügbaren Sitzungstage
for (i in 1:nrow(records)) {
  
  # Datum des jeweiligen Sitzungstags extrahieren (Format: YYYY-MM-DD)
  datum <- substr(records$issueDate[i], 1, 10)
  
  # Detail-URL für den jeweiligen Sitzungstag zusammensetzen
  detail_url <- paste0(records$url[i], "&api_key=", api_key)
  
  # Fehlerbehandlung: Skript läuft bei Fehlern weiter
  try({
    res <- GET(detail_url)
    tages_details <- fromJSON(content(res, "text", encoding = "UTF-8"))
    
    # 1. Bedingung: Gesamtausgabe als PDF herunterladen (entireIssue)
    if (!is.null(tages_details$issue$fullIssue$entireIssue)) {
      final_url <- tages_details$issue$fullIssue$entireIssue$url[1]
      dateiname <- paste0("Full_Record_", datum, ".pdf")
      download.file(final_url, destfile = dateiname, mode = "wb", quiet = TRUE)
      message("Volltext geladen (PDF): ", dateiname)
      
      # 2. Bedingung: Einzelne Sektionen als HTML oder PDF herunterladen
    } else if (!is.null(tages_details$issue$fullIssue$sections)) {
      sektionen <- tages_details$issue$fullIssue$sections
      
      # Schleife über alle Sektionen des Sitzungstags
      for (j in 1:nrow(sektionen)) {
        
        # HTML-Version bevorzugen (Formatted Text), sonst PDF als Fallback
        text_index <- which(sektionen$text[[j]]$type == "Formatted Text")[1]
        if (is.na(text_index)) text_index <- which(sektionen$text[[j]]$type == "PDF")[1]
        
        final_url <- sektionen$text[[j]]$url[text_index]
        
        # Dateiendung anhand der URL bestimmen
        ext <- ifelse(grepl(".htm", final_url), ".html", ".pdf")
        sek_name <- paste0("Record_", datum, "_", gsub(" ", "_", sektionen$name[j]), ext)
        download.file(final_url, destfile = sek_name, mode = "wb", quiet = TRUE)
        message("Sektion geladen: ", sek_name)
      }
    }
    
    # Pause zwischen Anfragen um IP-Block zu vermeiden
    Sys.sleep(0.5)
    
  }, silent = TRUE)
}