# School Schedule API

A Django REST Framework application that manages school schedules, providing endpoints to view and filter class schedules, with built-in performance optimizations for handling large datasets.

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Make

### Running the Project

```bash
# First time setup(build + migrate + populate_data + up)
make initial_start

# Clean up containers and volumes
make clean
```

### Running Tests

```bash
make test
```

### Development Setup

#### Pre-commit Hooks

We use pre-commit hooks to ensure code quality. To set up:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run against all files (optional)
pre-commit run --all-files
```

The hooks will run automatically on `git commit`. They include:
- Black (code formatting)
- Flake8 (code linting)
- isort (import sorting)
- Various file checks (trailing whitespace, EOF)

## Performance Optimizations

### 1. Database Optimizations
- **Select Related**: Using `select_related` to avoid N+1 queries when fetching related models (teacher, subject, class)
- **New db field** `student_count`: This field is updated by signals when a student is created/deleted/updated. By doing this, we avoid N+1 on the schedule view.
- **Unique Constraints**: Implemented model constraints to maintain data integrity and improve query performance

### 2. Caching Strategy
- **High-Level Caching**: Implemented view-level caching since schedule data rarely changes
- **Backend**: Using Redis
- **Cache Invalidation**: Invalidation only when schedule-related data changes
- **Cache Keys**: URL-based cache keys to handle different filter combinations

### 3. API Optimizations
- **Pagination**: Implemented limit/offset pagination to handle large datasets efficiently

## Future Optimizations or Improvements

1. **Database**
   - Consider read replicas for scaling since this application is read-heavy

2. **Caching**
   - Optimize cache keys when filters are in a different order

3. **Testing**
   - Add more tests for the API
   - Add more tests for the database
   - Use locust for load testing

4. **Logging**
   - Add logging for the API, setup a middleware to log requests and responses

5. **Search & Filtering**
    - Consider Elasticsearch for complex filtering scenarios:
      - Better performance for complex filter combinations

6. **Deployment**
   - Setup gunicorn + wsgi + nginx
   - I will try to deploy this application to AWS ECS and see how to achieve orizontal/vertical scaling
   - Setup CI/CD pipeline to deploy the application
