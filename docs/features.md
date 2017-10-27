Features
========

### Structured Data

#### Monotonic numeric features:

- `bedrooms`
- `bathrooms`
- `sqft`

#### Boolean features:

- `apartment`
- `assisted living`
- `attached garage`
- `carport`
- `cats are OK - purrr`
- `condo`
- `cottage/cabin`
- `detached garage`
- `dogs are OK - wooof`
- `duplex`
- `flat`
- `furnished`
- `house`
- `in-law`
- `land`
- `laundry in bldg`
- `laundry on site`
- `manufactured`
- `no laundry on site`
- `no parking`
- `no smoking`
- `off-street parking`
- `street parking`
- `townhouse`
- `valet parking`
- `w/d hookups`
- `w/d in unit`
- `wheelchair accessible`

#### Aggregated boolean features:

- Housing type
  - `apartment`
  - `condo`
  - `cottage/cabin`
  - `duplex`
  - `flat`
  - `house`
  - `in-law`
  - `land`
  - `manufactured`
  - `townhouse`
- Parking
  - `attached garage`
  - `carport`
  - `detached garage`
  - `no parking`
  - `off-street parking`
  - `street parking`
  - `valet parking`
- Laundry
  - `laundry in bldg`
  - `laundry on site`
  - `no laundry on  site`
  - `w/d hookups`
  - `w/d in unit`
- Pets
  - `cats are OK - purrr`
  - `dogs are OK - wooof`
- Other
  - `assisted living`
  - `no smoking`
  - `wheelchair accessible`

#### Location features:

- `latitude`
- `longitude`

#### Text data:

- `description`
- `title`

#### Meta data:

- `_id`
- `listing_id`
- `num_images`
- `zipcode`

### Engineered Features

> Brainstorming

#### Description meta data:

- `flesch_reading_ease` - 0-100 scale for readability
- `smog_index`
- `flesch_kincaid_grade` - grade level
- `coleman_liau_index`
- `automated_readability_index`
- `dale_chall_readability_score`
- `difficult_words` - count of difficult words in doc
- `linsear_write_formula`
- `gunning_fog`
- `text_standard` - grade level range
- Length of the description

#### Extracted (extra) features from description:

- Neighborhood
  - Have a set of neighborhood names and match on it
- Public transit information
  - Link
  - Bus
  - Public transit
  - Other similar keywords
- Keywords
  - Modern
  - View
  - New
  - Remodeled
- Parking cost

#### Extracted (duplicate) features from description:

- Bedrooms/bathrooms
- Square feet
- Pet info
  - Look for other kinds of pets
- Laundry info
- Housing type
  - Augment with 'studio'
- Parking type

### Next steps

Need to build actual python modules.

- Add text stats to the units collection
- Dig out specific features that aren't structured attributes
- Find features that *are* in the structured attributes

Add features one at a time and see what the effect is.

- Build an MVP website that takes a Craigslist link and runs it through the
model
- Don't need to add a ton of features