# Example Run: Contract Diff

- Removed `DELETE /users/{id}` method -> breaking.
- Added required field `email` in `POST /users` request body -> potentially breaking.
- Recommendation: block release until versioning strategy is updated.
