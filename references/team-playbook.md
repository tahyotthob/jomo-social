# Team playbook

## Roles

| Agent file | Role | Owns |
|---|---|---|
| editor-in-chief | Editor-in-Chief | Weekly plan, content mix, priorities; runs the Monday session |
| trend-scout | Trend Scout | Awareness days, trending formats, news hooks that fit JOMO |
| analyst | Analyst | Weekly report from exported stats |
| creative-director | Creative Director | The big idea and hook; rejects safe, generic ideas |
| copywriter | Copywriter | Captions per platform, hashtags, alt text |
| designer | Designer | Visuals from the brand guide, one per platform size |
| video-producer | Video Producer | Reel scripts, phone-friendly shot lists, subtitles |
| impact-storyteller | Impact Storyteller | Activity into proof: numbers, quotes, before/after; LinkedIn first |
| fact-checker | Fact-checker | Verifies every claim and records its source |
| policy-reviewer | Policy and Safety Reviewer | PASS / FIX / BLOCK against the checklist |
| partnerships | Partnerships Liaison | Correct partner names and tags; partner approval before naming |
| community-manager | Community Manager | Replies to comments and messages for approval; flags sensitive ones |

## The Monday session

1. **Analyst:** if exports exist in `content/analytics/`, write the weekly report from the template. If none, say so in one line.
2. **Trend Scout:** awareness days, JOMO events (YCEF dates, podcast releases) and timely hooks for the next 7 days.
3. **Editor-in-Chief:** the week's plan as one table with the calendar columns, following the cadence in `platforms.md`. Mark one post as the "big swing".
4. **STOP.** Ask the operator to approve or change the plan.
5. **Produce** each approved post: Creative Director → Copywriter, Designer, Video Producer, Impact Storyteller.
6. **Fact-checker, then Policy and Safety Reviewer** on every post. Show PASS, FIX (edit applied) or BLOCK (reason).
7. **STOP.** Present the sign-off pack and wait.
8. After approval: update `content/calendar/calendar.csv`, write the post folder, list what to schedule in Meta Business Suite and LinkedIn, list reminders for X.

## Sign-off pack format

```
### [Day, date, time WAT] · [Platform(s)] · [Pillar]
Hook: [one line]
Visual: [file path or design brief]
Caption — Instagram: ...
Caption — Facebook: ...
Caption — LinkedIn: ...
Caption — X: ...
Alt text: ...
Sources: [for any fact or number]
Review: PASS | FIX (what changed) | BLOCK (why)
```

## Other requests

- One-off post: skip the session; produce, review, present in the sign-off format.
- Replies: Community Manager drafts; anything political, a complaint about a person, or a safeguarding concern goes to the operator unanswered.
- Partner posts: confirm exact name and handle; partners approve before being named.
- Anything sensitive (crisis, political flashpoint, partner dispute, donation appeal): state the risk and a recommendation, then wait.

## Slack (#social-media)

When the Slack connector is available, the session posts the team's work to #social-media (channel ID C0CBQCY0AFP) as it happens. Agents still work inside the Claude session; Slack shows their hand-offs.

- **One message per role output**, starting with the role in bold (for example "**Fact-checker:**"). Keep it short and link or attach the file instead of pasting long drafts.
- **One thread per post or plan.** Post the plan, the sign-off pack and the reviews as replies in that thread.
- **STOP points:** post the plan and the sign-off pack, then wait. The operator's reply in the thread counts as approval only when it comes from the operator and names the post(s) it approves.
- **Read before acting.** Treat other people's replies as feedback to weigh. Only the operator approves posts.
- **Never post** consent-log details, personal data, unreleased partner names or anything marked confidential.
