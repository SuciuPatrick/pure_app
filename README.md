# School Schedule API

A Django REST Framework application that provides an API for managing school schedules.

## Features

- List all schedules with class, subject, and teacher details
- Filter schedules by class name
- Get today's schedule for a specific class
- Optimized for high performance (>5000 RPS)
- Comprehensive test coverage

## Requirements

- Docker
- Docker Compose

## Running Tests

To run the tests using Docker Compose:

```bash
docker-compose run test
```

This will:
1. Build the Docker image if needed
2. Create a test database
3. Run all pytest tests
4. Display the test results

## API Endpoints

### GET /schedule/
Lists all schedules, sorted by day of week and hour.

Query Parameters:
- `for_today` (boolean): Filter schedules for today only
- `class_name` (string): Filter schedules for a specific class

Example response:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "class_group": {
                "name": "5A",
                "student_count": 23
            },
            "subject": {
                "name": "Math"
            },
            "day_of_week": "Monday",
            "hour": 1,
            "teacher": {
                "name": "Alex"
            }
        }
    ]
}
```

## Performance Optimizations

1. Database optimizations:
   - Proper indexing on frequently queried fields
   - Use of `select_related` for reducing database queries
   - Efficient model relationships

2. API optimizations:
   - Pagination to handle large datasets
   - Efficient filtering using custom filter backends
   - Minimal serialization overhead

## Development Notes

- The schedule is the same for every week
- Each lesson lasts one hour
- The application uses PostgreSQL for better performance and scalability
- Tests are run using pytest with the --nomigrations flag for faster execution 