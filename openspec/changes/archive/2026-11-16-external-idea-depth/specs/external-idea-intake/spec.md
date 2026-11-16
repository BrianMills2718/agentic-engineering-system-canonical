# external-idea-intake Specification

## ADDED Requirements

### Requirement: The usefulness judge reads more only when it asks to, and only what it asks for

For each post the judge SHALL return useful, not useful or need more (comments, linked pages or both). For need-more posts the command SHALL read exactly the requested material and the judge SHALL return a final verdict from it. The model SHALL NOT be given tools. Each useful post SHALL record what it was judged from.

#### Scenario: depth-judge-reads-more-when-asked

- **WHEN** the model asks for the comments of one post and marks another useful from its title
- **THEN** only that post's comments are read, the final verdict for it uses them, and the other post is recorded as judged from its title
