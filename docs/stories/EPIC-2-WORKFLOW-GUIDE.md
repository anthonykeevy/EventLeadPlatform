# Epic 2 Workflow Guide - Story-by-Story Agentic Development

**Purpose:** Complete workflow guide for Epic 2 development using story-by-story approach  
**Created:** January 15, 2025  
**For:** Anthony Keevy (Product Manager)  
**Status:** Ready to Use  

---

## 🎯 **Workflow Overview**

This guide provides the exact prompts and processes for Epic 2 development using a story-by-story approach optimized for agentic programming. Each stage has specific prompts and expected outcomes.

---

## 📋 **Stage 1: Starting a New Story**

### **When to Use**
- Beginning Epic 2
- Starting next story in sequence
- Moving to next domain

### **Prompt to Use**
```
@sm.mdc Please create the next Epic 2 story. 

Current Status:
- Epic 2 Status: docs/stories/EPIC-2-STATUS.md
- Last Completed Story: [Story ID or "None"]
- Current Domain: [Domain Name]
- Next Story Needed: [Story Title or "Next in sequence"]

Requirements:
- Create story file in docs/stories/ folder
- Create context file in docs/stories/ folder  
- Update Epic 2 Status document
- Ensure story includes comprehensive UAT tests
- Focus on [Domain Name] domain
- Follow BMAD v6 story creation standards
- Include creation summary for quality assurance

Expected Deliverables:
1. Story file: docs/stories/story-2.X.md
2. Context file: docs/stories/story-context-2.X.xml
3. Epic 2 Status update
4. Creation summary (BMAD standard)

Please confirm story creation and provide story ID.
```

### **Expected Outcome**
- Story file created: `docs/stories/story-2.X.md`
- Context file created: `docs/stories/story-context-2.X.xml`
- Epic 2 Status updated
- Creation summary document created
- Story ready for implementation

### **Common Issue: Database Tasks**
**Problem:** Stories may include database setup tasks even when database is already ready
**Solution:** When implementing story, inform Developer Agent that database tasks are complete but need verification
**Example:** "Database migrations are complete up to 018_logging_configuration.py - please verify and skip setup tasks"

---

## 🔧 **Stage 2: Story Implementation**

### **When to Use**
- Story has been created and is ready for implementation
- Developer Agent needs to begin work

### **Prompt to Use**
```
@dev.mdc Please implement Epic 2 Story 2.X: [Story Title]

Story Location: docs/stories/story-2.X.md
Context Location: docs/stories/story-context-2.X.xml
Epic 2 Status: docs/stories/EPIC-2-STATUS.md

Database Status:
- Epic 1 migrations: Complete (002_epic1_complete_schema.py)
- Epic 2 migrations: Complete up to 018_logging_configuration.py
- Database is ready - verify and skip any database setup tasks
- Focus on testing existing database functionality

Requirements:
- Implement all story requirements
- Verify database functionality (skip setup tasks)
- Perform QA testing (backend/frontend as applicable)
- Conduct UAT testing (if frontend story)
- Update story file with implementation details
- Mark UAT tests as completed/passed
- Add reflection and lessons learned
- Update Epic 2 Status document

Focus Areas:
- [Specific requirements from story]
- [Domain-specific considerations]
- [Integration points with Epic 1]

Please confirm completion and provide implementation summary.
```

### **Expected Outcome**
- Story fully implemented
- QA testing completed
- UAT testing completed (if applicable)
- Story file updated with completion report
- Epic 2 Status updated

---

## 📊 **Stage 3: Story Completion Report**

### **When to Use**
- Story implementation is complete
- Developer Agent needs to finalize story

### **Prompt to Use**
```
@dev.mdc Please complete the Epic 2 Story 2.X completion report.

Story Location: docs/stories/story-2.X.md
Epic 2 Status: docs/stories/EPIC-2-STATUS.md

Requirements:
- Update story file with detailed completion report
- Mark all UAT tests as completed/passed
- Document what was implemented
- Record any issues found and fixed
- Add lessons learned and improvements
- Update Epic 2 Status document with story completion
- Identify next story needed (if applicable)

Completion Report Should Include:
- Implementation summary
- APIs created/modified
- Database changes
- Frontend components
- Testing results
- Issues resolved
- Lessons learned
- What could be improved

Please confirm completion report is finished.
```

### **Expected Outcome**
- Story file updated with comprehensive completion report
- All UAT tests marked as completed/passed
- Epic 2 Status updated with story completion
- Next story identified (if applicable)

---

## 📈 **Stage 4: Epic 2 Status Update**

### **When to Use**
- After each story completion
- When checking Epic 2 progress
- Before starting next story

### **Prompt to Use**
```
@pm.mdc Please update the Epic 2 Status document.

Current Status:
- Last Completed Story: 2.X - [Story Title]
- Next Story: 2.Y - [Story Title]
- Current Domain: [Domain Name]
- Epic Progress: [X/12 stories complete]

Requirements:
- Update Epic 2 Status document
- Review story completion history
- Update progress metrics
- Identify next story needed
- Check domain completion status
- Provide recommendations for next steps

Focus Areas:
- [Current domain progress]
- [Dependencies and blockers]
- [Quality and performance trends]
- [Process improvements identified]

Please confirm status update and provide next recommendations.
```

### **Expected Outcome**
- Epic 2 Status document updated
- Progress metrics current
- Next story identified
- Recommendations provided

---

## 🔍 **Stage 5: Domain Review**

### **When to Use**
- All stories in a domain are complete
- Before moving to next domain
- For comprehensive reflection and learning

### **Prompt to Use**
```
@pm.mdc Please conduct a comprehensive Domain [X] review for Epic 2.

Domain: [Domain Name]
Stories Completed: [List of story IDs]
Domain Status: Complete

Requirements:
- Create domain review document: docs/stories/DOMAIN-[X]-[NAME]-REVIEW.md
- Analyze all stories in domain
- Review UAT test results
- Identify common issues and patterns
- Document lessons learned
- Recommend process improvements
- Update Epic 2 Status with domain completion
- Prepare for next domain

Review Should Include:
- Domain completion summary
- UAT test analysis
- Performance impact assessment
- Common issues identified
- Process improvements recommended
- Technical debt assessment
- Next domain preparation

Please confirm domain review is complete.
```

### **Expected Outcome**
- Domain review document created
- Comprehensive analysis completed
- Process improvements identified
- Epic 2 Status updated with domain completion
- Next domain prepared

---

## 🚀 **Stage 6: Epic 2 Retrospective**

### **When to Use**
- All Epic 2 stories are complete
- All domains are complete
- Ready for Epic 3 planning

### **Prompt to Use**
```
@pm.mdc Please conduct Epic 2 retrospective and prepare Epic 3 recommendations.

Epic 2 Status: Complete
All Stories: 12/12 Complete
All Domains: 4/4 Complete

Requirements:
- Create Epic 2 retrospective document
- Analyze all story completion reports
- Review all domain reviews
- Identify process improvements
- Assess Epic 2 success criteria
- Prepare Epic 3 recommendations
- Update project documentation

Retrospective Should Include:
- Epic 2 success assessment
- Process effectiveness analysis
- Quality metrics review
- Performance impact analysis
- Lessons learned summary
- Process improvements for Epic 3
- Epic 3 readiness assessment

Please confirm retrospective is complete.
```

### **Expected Outcome**
- Epic 2 retrospective document created
- Process improvements identified
- Epic 3 recommendations prepared
- Project documentation updated

---

## 📁 **File Structure**

### **Stories Location**
```
docs/stories/
├── EPIC-2-STATUS.md                    # Epic 2 status tracking
├── EPIC-2-WORKFLOW-GUIDE.md           # This workflow guide
├── story-2.1.md                        # Story 2.1 file
├── story-2.2.md                        # Story 2.2 file
├── story-context-2.1.xml               # Story 2.1 context
├── story-context-2.2.xml               # Story 2.2 context
├── DOMAIN-1-USER-EXPERIENCE-REVIEW.md  # Domain 1 review
├── DOMAIN-2-EVENT-MANAGEMENT-REVIEW.md # Domain 2 review
├── DOMAIN-3-FORM-FOUNDATION-REVIEW.md  # Domain 3 review
└── DOMAIN-4-APPROVAL-WORKFLOWS-REVIEW.md # Domain 4 review
```

---

## 🎯 **Quality Gates**

### **Story Completion Criteria**
- ✅ All story requirements implemented
- ✅ QA testing completed and passed
- ✅ UAT testing completed and passed (if applicable)
- ✅ Story file updated with completion report
- ✅ Epic 2 Status updated

### **Domain Completion Criteria**
- ✅ All domain stories completed
- ✅ Comprehensive UAT testing completed
- ✅ Domain review document created
- ✅ Process improvements identified
- ✅ Next domain prepared

### **Epic Completion Criteria**
- ✅ All 12 stories completed
- ✅ All 4 domains completed
- ✅ Epic 2 retrospective completed
- ✅ Epic 3 recommendations prepared

---

## 🔄 **Process Flow**

```
1. Start Story → Create Story + Context
2. Implement Story → QA + UAT Testing
3. Complete Story → Update with Reflection
4. Update Status → Track Progress
5. Domain Complete → Domain Review
6. Epic Complete → Epic Retrospective
```

---

## 💡 **Best Practices**

### **Story Creation**
- Focus on one story at a time
- Ensure comprehensive UAT tests
- Include clear acceptance criteria
- Consider domain dependencies

### **Implementation**
- Follow Epic 1 patterns and standards
- Maintain performance characteristics
- Ensure backward compatibility
- Document all changes

### **Testing**
- QA testing for all stories
- UAT testing for frontend stories
- Integration testing for cross-domain stories
- Performance testing for critical paths

### **Reflection**
- Document what was implemented
- Record issues and fixes
- Identify lessons learned
- Suggest improvements

---

## 🚨 **Troubleshooting**

### **Common Issues**
- **Story not ready:** Check dependencies and prerequisites
- **UAT failures:** Review test cases and implementation
- **Performance issues:** Check Epic 1 baseline and optimization
- **Integration problems:** Verify cross-domain communication

### **Escalation**
- **Technical issues:** Developer Agent troubleshooting
- **Process issues:** Product Manager guidance
- **Quality issues:** Review UAT test cases and requirements

---

*Epic 2 Workflow Guide - Generated by BMAD Product Manager Agent*  
*Date: 2025-01-15*  
*Status: Ready to Use*
