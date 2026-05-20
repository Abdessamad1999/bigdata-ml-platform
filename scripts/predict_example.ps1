$body = @{
  amount_log = 5.3
  hour_sin = -0.7
  hour_cos = 0.2
  merchant_risk = 0.82
  account_age_score = 1.0
  country_risk = 0.65
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/predict" -ContentType "application/json" -Body $body

