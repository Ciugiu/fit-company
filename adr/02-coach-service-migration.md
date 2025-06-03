# Coach Service Migration

###### Warning

The openapi yaml in `docs/openapi.yaml` was done using ai.

## Why

WOD generation is slow in the monolith. We want to move it to a new "coach" microservice, but we can’t have downtime.

## Steps

1. Move WOD code to a shared file so both apps can use it.
2. Build the coach microservice with a `/generate-wod` endpoint.
3. Coach asks the monolith for yesterday’s exercise history before making a WOD.
4. Add a new endpoint in the monolith that sends WOD requests to the coach.
5. Later, make the old `/fitness/wod` endpoint also use the coach.
6. Use Docker Compose to run both services.
7. Test with k6 to make sure it works well.

## Why this way

- No downtime: both old and new ways work during migration.
- Coach only makes WODs, doesn’t store history.
- Easy to scale coach service.

## Risks

- If coach can’t reach monolith, WODs can fail.
- Both services must agree on data format.

## Rollback

- If there’s a problem, switch back to the old WOD code in the monolith.