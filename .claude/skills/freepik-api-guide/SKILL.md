---
name: freepik-api-guide
description: Use this skill when working with the Freepik Stock Content API. This includes searching for stock images, understanding filter options, constructing effective queries, handling pagination, and working with license types. The skill provides reference information about API endpoints, request parameters, response formats, and best practices for efficient API usage.

Examples:
<example>
Context: User wants to find images for a website hero section
user: "I need a hero image for my landing page"
assistant: "I'll use the Freepik API to find suitable hero images. Based on your needs, I'll search for horizontal orientation photos that would work well as banner images."
<commentary>
The skill is triggered because the user needs stock images, which requires understanding the Freepik API's search capabilities, orientation filters, and content types.
</commentary>
</example>

<example>
Context: User is confused about Freepik API license types
user: "What's the difference between free and premium resources?"
assistant: "Freepik offers different license types. Free resources can be used without attribution but may have limitations. Premium resources require an active subscription. Let me search and show you the license information for specific resources."
<commentary>
The skill is triggered because understanding license types is core knowledge provided by this skill, and the user needs guidance on usage rights.
</commentary>
</example>

<example>
Context: Agent is building a search query
user: "Find me some good business meeting photos"
agent: "I'll construct an effective search query using the Freepik API. For business contexts, I should use keywords like 'business meeting' combined with type='photo' and orientation='horizontal' filters for best results."
<commentary>
The skill is triggered because the agent needs knowledge about search query patterns and filter combinations to construct an effective API request.
</commentary>
</example>
---

You are the Freepik API Guide, providing expertise on the Freepik Stock Content API.

## API Overview

The Freepik Stock Content API provides access to millions of stock resources including photos, vectors, illustrations, PSD templates, and icons.

**Base URL:** `https://api.freepik.com`
**Authentication:** `x-freepik-api-key` header
**Rate Limits:** Tracked via response headers, implement backoff on 429

## Core Endpoints

### Search Resources
```
GET /v1/resources
```
**Parameters:**
- `query` (required): Search keywords
- `type`: photo | vector | psd | illustration
- `orientation`: horizontal | vertical | square
- `license`: free | premium | attribution
- `page`: Page number (default: 1)
- `limit`: Results per page (recommended: 10-20)

**Response:** Array of resource objects with id, title, url, type, is_premium

### Get Resource Details
```
GET /v1/resources/{id}
```
**Response:** Full resource metadata including description, dimensions, license info

### Download Resource
```
GET /v1/resources/{id}/download
```
**Response:** Download URL and filename

### Browse Icons
```
GET /v1/icons
```
**Parameters:**
- `query`: Search term (optional)
- `style`: filled | outline | rounded | sharp | 2d | 3d
- `page`: Page number

## Effective Search Patterns

### For Website Headers
- Query: "hero banner" or "header background"
- Filters: `orientation=horizontal`, `type=photo`
- Best for: Landing pages, blog headers

### For Social Media
- Query: "social media post" or specific topic
- Filters: `orientation=square` (Instagram) or `orientation=vertical` (Stories)
- Best for: Posts, stories, covers

### For Presentations
- Query: "business presentation" or "corporate background"
- Filters: `orientation=horizontal`, `type=illustration` or `psd`
- Best for: Slide backgrounds, business decks

### For UI Design
- Query: Specific icon names + "icon"
- Use `/v1/icons` endpoint
- Filter by `style`: filled, outline, rounded

### For Avatars/Profiles
- Query: "portrait" or "profile picture"
- Filters: `orientation=vertical`, `type=photo`
- Best for: User profiles, team pages

## Filter Combinations

### By Content Type
- `type=photo` - Real photographs, best for realistic content
- `type=vector` - Scalable graphics, ideal for logos and icons
- `type=psd` - Layered Photoshop files, for design customization
- `type=illustration` - Digital artwork, for creative content

### By Orientation
- `orientation=horizontal` - 16:9 or similar, best for headers/banners
- `orientation=vertical` - 9:16 or similar, best for mobile/stories
- `orientation=square` - 1:1 ratio, best for avatars/thumbnails

### By License
- `license=free` - No payment required, check attribution needs
- `license=premium` - Requires subscription, full rights
- `license=attribution` - Free but must credit creator

## Pagination Best Practices

1. **Start with page 1** to gauge result quality
2. **Use small page sizes** (10-20) to minimize context usage
3. **Refine with filters** rather than paging through many results
4. **Monitor rate limits** via response headers
5. **Cache results** when possible to avoid redundant searches

## Rate Limit Handling

The API returns rate limit information in headers:
- `x-rate-limit-remaining`: Requests left
- `x-rate-limit-reset`: Unix timestamp when limit resets

**Best practices:**
- Implement exponential backoff on HTTP 429
- Cache search results for repeated queries
- Use specific filters to reduce pagination needs

## License and Attribution

Always check the license field before using images:
- **Free**: May be used without payment, check if attribution needed
- **Premium**: Requires active Freepik subscription
- **Attribution Required**: Must credit the creator when used

Refer to https://www.freepik.com/license for detailed terms.

## Common Error Codes

- `401`: Invalid API key
- `429`: Rate limit exceeded, implement backoff
- `404`: Resource not found
- `400`: Invalid request parameters

## Output Optimization

To minimize context usage:
1. Request only needed fields
2. Use small page sizes (default: 10)
3. Truncate long descriptions in responses
4. Use specific queries rather than broad searches

For detailed information, see:
- `references/endpoints.md` - Complete API endpoint reference
- `references/filters.md` - Detailed filter documentation
- `examples/search-queries.md` - Real-world query examples
