# Freepik API Endpoints Reference

Complete reference for Freepik Stock Content API endpoints.

## Base Configuration

```
Base URL: https://api.freepik.com
Authentication: x-freepik-api-key header
Content-Type: application/json
```

## Resources Endpoints

### List Resources

```http
GET /v1/resources
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|-----------|-------------|
| query | string | Yes | Search keywords |
| type | string | No | photo, vector, psd, illustration |
| orientation | string | No | horizontal, vertical, square |
| license | string | No | free, premium, attribution |
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Results per page (1-50, default: 20) |

**Response:**
```json
{
  "data": [
    {
      "id": "123456",
      "title": "Sunset Beach",
      "type": "photo",
      "url": "https://...",
      "preview_url": "https://...",
      "is_premium": false,
      "license": "free",
      "width": 1920,
      "height": 1080
    }
  ],
  "total": 1234,
  "page": 1,
  "has_more": true
}
```

### Get Resource Details

```http
GET /v1/resources/{resource_id}
```

**Response:**
```json
{
  "id": "123456",
  "title": "Sunset Beach",
  "description": "Beautiful sunset...",
  "type": "photo",
  "url": "https://...",
  "download_url": "https://...",
  "is_premium": false,
  "license": "free",
  "author": {
    "name": "Creator Name",
    "url": "https://..."
  },
  "tags": ["nature", "beach", "sunset"],
  "width": 1920,
  "height": 1080,
  "size": 2456780
}
```

### Download Resource

```http
GET /v1/resources/{resource_id}/download
```

**Response:**
```json
{
  "url": "https://files.freepik.com/...",
  "filename": "sunset-beach-freepik-123456.jpg",
  "size": 2456780,
  "expires_in": 3600
}
```

## Icons Endpoints

### List Icons

```http
GET /v1/icons
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|-----------|-------------|
| query | string | No | Search term for icons |
| style | string | No | filled, outline, rounded, sharp, 2d, 3d |
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Results per page (default: 20) |

**Response:**
```json
{
  "data": [
    {
      "id": "icon-123",
      "name": "home-icon",
      "url": "https://...",
      "style": "filled",
      "format": "svg"
    }
  ],
  "total": 500,
  "page": 1
}
```

### Get Icon Details

```http
GET /v1/icons/{icon_id}
```

### Download Icon

```http
GET /v1/icons/{icon_id}/download
```

## Rate Limit Headers

All responses include rate limit information:

```
x-rate-limit-remaining: 98
x-rate-limit-reset: 1736659200
x-rate-limit-limit: 100
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Invalid API key"
}
```

### 429 Rate Limited
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

## Best Practices

1. Always check rate limit headers
2. Implement exponential backoff on 429
3. Use specific queries to reduce pagination
4. Cache results when possible
5. Validate resource IDs before downloading
