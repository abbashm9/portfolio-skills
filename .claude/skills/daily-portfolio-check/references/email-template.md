# HTML Email Template

Use this structure for every daily report. Inline CSS only — email clients strip `<style>` tags. Use tables for layout — flexbox/grid don't work in most email clients.

## Color palette

```
Background:       #f4f5f7
Card background:  #ffffff
Border:           #e5e7eb
Text primary:     #111827
Text secondary:   #6b7280
Text muted:       #9ca3af

Positive (green): #059669 (text) / #d1fae5 (bg)
Negative (red):   #dc2626 (text) / #fee2e2 (bg)
Watch (yellow):   #d97706 (text) / #fef3c7 (bg)
Action (orange):  #ea580c (text) / #ffedd5 (bg)
Alert (red bold): #b91c1c (text) / #fecaca (bg)

Education box:    #1e293b (text) / #f1f5f9 (bg)
Accent (link):    #2563eb
```

## Full email structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f4f5f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; color: #111827;">

<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f4f5f7; padding: 24px 12px;">
  <tr>
    <td align="center">
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden;">
        
        <!-- HERO BANNER -->
        <tr>
          <td style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 32px 24px; color: #ffffff;">
            <p style="margin: 0; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #94a3b8;">Daily Portfolio Check</p>
            <p style="margin: 4px 0 16px 0; font-size: 14px; color: #cbd5e1;">[Day, Month Date, Year — Kuwait time]</p>
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
              <tr>
                <td>
                  <p style="margin: 0; font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Total P&L</p>
                  <p style="margin: 4px 0 0 0; font-size: 36px; font-weight: 700; color: [#10b981 if positive, #ef4444 if negative];">[+$XX.XX] <span style="font-size: 18px; opacity: 0.8;">([+X.XX%])</span></p>
                </td>
                <td align="right" valign="bottom">
                  <p style="margin: 0; font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Today</p>
                  <p style="margin: 4px 0 0 0; font-size: 18px; font-weight: 600; color: [color]">[+$X.XX] ([+X.X%])</p>
                </td>
              </tr>
            </table>
            
            <p style="margin: 16px 0 0 0; padding-top: 16px; border-top: 1px solid #475569; font-size: 13px; color: #e2e8f0;">[Headline event of the day in 1 sentence]</p>
          </td>
        </tr>
        
        <!-- DECISIONS NEEDED (only if any) -->
        <tr>
          <td style="padding: 16px 24px; background-color: #fef3c7; border-bottom: 1px solid #fde68a;">
            <p style="margin: 0; font-size: 11px; font-weight: 600; color: #92400e; text-transform: uppercase; letter-spacing: 0.5px;">⚠️ Decisions needed</p>
            <p style="margin: 6px 0 0 0; font-size: 14px; color: #78350f;">[E.g.: "NVDA earnings May 20 — make trim/hold/exit call by Friday May 16"]</p>
          </td>
        </tr>
        
        <!-- POSITION SNAPSHOT TABLE -->
        <tr>
          <td style="padding: 24px;">
            <p style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">Position Snapshot</p>
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse: collapse; font-size: 13px;">
              <thead>
                <tr style="background-color: #f9fafb;">
                  <th style="text-align: left; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">Status</th>
                  <th style="text-align: left; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">Ticker</th>
                  <th style="text-align: right; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">Close</th>
                  <th style="text-align: right; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">Day</th>
                  <th style="text-align: right; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">P&L $</th>
                  <th style="text-align: right; padding: 10px 8px; font-weight: 600; color: #6b7280; border-bottom: 1px solid #e5e7eb;">P&L %</th>
                </tr>
              </thead>
              <tbody>
                <!-- ONE ROW PER POSITION -->
                <tr>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6;">
                    <span style="display: inline-block; padding: 2px 8px; background-color: [status bg]; color: [status text]; border-radius: 10px; font-size: 11px; font-weight: 600;">[✅ HOLD / ⚠️ WATCH / 🔔 ACTION / 🚨 ALERT]</span>
                  </td>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6; font-weight: 600;">NVDA</td>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6; text-align: right; font-variant-numeric: tabular-nums;">$XXX.XX</td>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6; text-align: right; color: [green/red]; font-variant-numeric: tabular-nums;">+X.XX%</td>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6; text-align: right; color: [green/red]; font-variant-numeric: tabular-nums;">+$X.XX</td>
                  <td style="padding: 12px 8px; border-bottom: 1px solid #f3f4f6; text-align: right; color: [green/red]; font-weight: 600; font-variant-numeric: tabular-nums;">+X.XX%</td>
                </tr>
                <!-- repeat for each position -->
                
                <!-- TOTAL ROW -->
                <tr style="background-color: #f9fafb;">
                  <td colspan="2" style="padding: 12px 8px; font-weight: 700;">TOTAL</td>
                  <td style="padding: 12px 8px; text-align: right; color: #6b7280;">—</td>
                  <td style="padding: 12px 8px; text-align: right; font-weight: 600; color: [color]; font-variant-numeric: tabular-nums;">[X.X%]</td>
                  <td style="padding: 12px 8px; text-align: right; font-weight: 700; color: [color]; font-variant-numeric: tabular-nums;">[$XX.XX]</td>
                  <td style="padding: 12px 8px; text-align: right; font-weight: 700; color: [color]; font-variant-numeric: tabular-nums;">[X.XX%]</td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        
        <!-- PER-POSITION DETAIL CARDS -->
        <tr>
          <td style="padding: 0 24px 24px 24px;">
            <p style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">Position Detail</p>
            
            <!-- ONE CARD PER POSITION -->
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 12px;">
              <tr>
                <td style="padding: 14px 16px;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td>
                        <span style="font-size: 16px; font-weight: 700;">NVDA</span>
                        <span style="margin-left: 8px; padding: 2px 8px; background-color: [status bg]; color: [status text]; border-radius: 10px; font-size: 11px; font-weight: 600;">[status]</span>
                      </td>
                      <td align="right" style="font-size: 14px; font-weight: 600;">
                        $XXX.XX <span style="color: [color]; font-size: 13px;">[+X.XX%]</span>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 8px 0 0 0; font-size: 13px; color: #4b5563; line-height: 1.5;">[1-2 sentence note on the position — what's happening, what to watch, any catalyst proximity]</p>
                  
                  <!-- Mini stops/TPs strip -->
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top: 10px;">
                    <tr>
                      <td style="font-size: 11px; color: #6b7280;">Stop: <span style="color: #111827; font-weight: 600;">$XXX</span></td>
                      <td style="font-size: 11px; color: #6b7280; text-align: center;">TP1: <span style="color: #111827; font-weight: 600;">$XXX</span></td>
                      <td style="font-size: 11px; color: #6b7280; text-align: center;">TP2: <span style="color: #111827; font-weight: 600;">$XXX</span></td>
                      <td style="font-size: 11px; color: #6b7280; text-align: right;">TP3: <span style="color: #111827; font-weight: 600;">$XXX</span></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <!-- repeat for each position -->
            
          </td>
        </tr>
        
        <!-- ROTATION SUGGESTIONS (only if any) -->
        <tr>
          <td style="padding: 0 24px 24px 24px;">
            <p style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">🔄 Rotation Suggestions</p>
            
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px;">
              <tr>
                <td style="padding: 12px 16px;">
                  <p style="margin: 0 0 4px 0; font-size: 13px; font-weight: 600; color: #1e40af;">Option A — [headline]</p>
                  <p style="margin: 0; font-size: 12px; color: #1e3a8a; line-height: 1.6;">
                    <strong>Sell:</strong> X.XXX shares NVDA at ~$XXX (~$XX freed)<br>
                    <strong>Buy:</strong> X.XXX shares MSFT at ~$XXX (~$XX)<br>
                    <strong>Why:</strong> [1 line rationale]<br>
                    <strong>Risk:</strong> [1 line risk]<br>
                    <em>Your call.</em>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        
        <!-- WHAT TO DO TOMORROW -->
        <tr>
          <td style="padding: 0 24px 24px 24px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
              <tr>
                <td style="padding: 16px 20px;">
                  <p style="margin: 0; font-size: 11px; color: #166534; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">What to do tomorrow</p>
                  <p style="margin: 6px 0 0 0; font-size: 14px; color: #14532d; line-height: 1.5;">[Clear, specific instruction. Often "no action needed, review Friday close" — that's a valid answer]</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        
        <!-- EDUCATION MODULE -->
        <tr>
          <td style="padding: 0 24px 24px 24px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f1f5f9; border-radius: 8px;">
              <tr>
                <td style="padding: 20px 24px;">
                  <p style="margin: 0; font-size: 11px; color: #475569; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">📚 Today you learned</p>
                  <p style="margin: 8px 0 0 0; font-size: 16px; font-weight: 700; color: #0f172a;">[Concept name]</p>
                  <p style="margin: 12px 0 0 0; font-size: 13px; color: #1e293b; line-height: 1.7;">
                    [80–120 word paragraph anchored to Abbas's actual positions and numbers]
                  </p>
                  <p style="margin: 12px 0 0 0; font-size: 12px; color: #475569; font-style: italic;">
                    Also today: [1-line mention of a related term]
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        
        <!-- FOOTER -->
        <tr>
          <td style="padding: 16px 24px 24px 24px; border-top: 1px solid #f3f4f6;">
            <p style="margin: 0; font-size: 10px; color: #9ca3af; line-height: 1.5;">
              Research output, not financial advice. Past performance does not guarantee future results. 
              Verify halal compliance quarterly on Zoya or Musaffa. Generated [timestamp] Kuwait time.
            </p>
          </td>
        </tr>
        
      </table>
    </td>
  </tr>
</table>

</body>
</html>
```

## Status badge colors quick reference

| Status | Text color | Background |
|--------|-----------|------------|
| ✅ HOLD | `#059669` | `#d1fae5` |
| ⚠️ WATCH | `#d97706` | `#fef3c7` |
| 🔔 ACTION | `#ea580c` | `#ffedd5` |
| 🚨 ALERT | `#b91c1c` | `#fecaca` |

## Number color rules

- Positive values: `#059669` (green)
- Negative values: `#dc2626` (red)
- Zero/flat: `#6b7280` (grey)

## Mobile considerations

- Keep email width at 600px max
- Use `font-variant-numeric: tabular-nums;` on all number cells so columns align
- Min font size 11px for non-critical text, 13px for body, 14–16px for headers
- Avoid horizontal scrolling — if table is too wide for mobile, collapse some columns

## What NOT to include

- No external image hosts (broken on some clients)
- No JavaScript (stripped by all clients)
- No `<style>` blocks in `<head>` (Gmail strips them)
- No emojis as critical info (use color/badges as primary signal)
- No fluff or extra commentary outside the structure
