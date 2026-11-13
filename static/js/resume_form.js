// Resume Creation and Editing Form Dynamic Row Handlers

document.addEventListener('DOMContentLoaded', function () {
  // 1. Profile Picture Preview
  const picInput = document.getElementById('id_profile_picture');
  const previewImg = document.getElementById('avatar-preview-img');

  if (picInput && previewImg) {
    picInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          previewImg.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // 2. Generic row removal using event delegation
  document.addEventListener('click', function (e) {
    const removeBtn = e.target.closest('.btn-remove-dynamic');
    if (removeBtn) {
      const card = removeBtn.closest('.dynamic-item-card');
      if (card) {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        setTimeout(() => card.remove(), 150);
      }
    }
  });

  // 3. Add Education Row
  const addEduBtn = document.getElementById('btn-add-education');
  const eduContainer = document.getElementById('education-container');
  if (addEduBtn && eduContainer) {
    addEduBtn.addEventListener('click', function () {
      const row = document.createElement('div');
      row.className = 'dynamic-item-card';
      row.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-primary"><i class="fa-solid fa-graduation-cap me-1"></i> Education</span>
          <button type="button" class="btn-remove-item btn-remove-dynamic" title="Remove education">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label small fw-semibold">Degree / Qualification *</label>
            <input type="text" name="education_degree[]" class="form-control" placeholder="e.g. B.Tech in Computer Science" required>
          </div>
          <div class="col-md-6">
            <label class="form-label small fw-semibold">College / Institute Name *</label>
            <input type="text" name="education_college[]" class="form-control" placeholder="e.g. ABC College of Engineering" required>
          </div>
          <div class="col-md-5">
            <label class="form-label small fw-semibold">University / Board</label>
            <input type="text" name="education_university[]" class="form-control" placeholder="e.g. State Technical University">
          </div>
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Graduation Year</label>
            <input type="text" name="education_year[]" class="form-control" placeholder="e.g. 2020 - 2024">
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">CGPA / Percentage</label>
            <input type="text" name="education_score[]" class="form-control" placeholder="e.g. 8.6 CGPA or 85%">
          </div>
        </div>
      `;
      eduContainer.appendChild(row);
    });
  }

  // 4. Add Experience Row
  const addExpBtn = document.getElementById('btn-add-experience');
  const expContainer = document.getElementById('experience-container');
  if (addExpBtn && expContainer) {
    addExpBtn.addEventListener('click', function () {
      const row = document.createElement('div');
      row.className = 'dynamic-item-card';
      row.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-primary"><i class="fa-solid fa-briefcase me-1"></i> Experience / Internship</span>
          <button type="button" class="btn-remove-item btn-remove-dynamic" title="Remove experience">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        <div class="row g-3">
          <div class="col-md-5">
            <label class="form-label small fw-semibold">Company / Organization *</label>
            <input type="text" name="experience_company[]" class="form-control" placeholder="e.g. Acme Tech Solutions" required>
          </div>
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Job Role / Title *</label>
            <input type="text" name="experience_role[]" class="form-control" placeholder="e.g. Python Developer Intern" required>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Duration *</label>
            <input type="text" name="experience_duration[]" class="form-control" placeholder="e.g. June 2023 - Present" required>
          </div>
          <div class="col-12">
            <label class="form-label small fw-semibold">Responsibilities & Highlights</label>
            <textarea name="experience_responsibilities[]" rows="2" class="form-control" placeholder="Key responsibilities and achievements (e.g. Developed REST APIs in Django, optimized database queries...)"></textarea>
          </div>
        </div>
      `;
      expContainer.appendChild(row);
    });
  }

  // 5. Add Project Row
  const addProjBtn = document.getElementById('btn-add-project');
  const projContainer = document.getElementById('project-container');
  if (addProjBtn && projContainer) {
    addProjBtn.addEventListener('click', function () {
      const row = document.createElement('div');
      row.className = 'dynamic-item-card';
      row.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-primary"><i class="fa-solid fa-laptop-code me-1"></i> Project</span>
          <button type="button" class="btn-remove-item btn-remove-dynamic" title="Remove project">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        <div class="row g-3">
          <div class="col-md-5">
            <label class="form-label small fw-semibold">Project Title *</label>
            <input type="text" name="project_title[]" class="form-control" placeholder="e.g. Online Resume Builder Web App" required>
          </div>
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Technologies Used *</label>
            <input type="text" name="project_tech[]" class="form-control" placeholder="e.g. Python, Django, MySQL, JavaScript" required>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Project Link (Optional)</label>
            <input type="text" name="project_link[]" class="form-control" placeholder="e.g. github.com/username/project">
          </div>
          <div class="col-12">
            <label class="form-label small fw-semibold">Project Description *</label>
            <textarea name="project_description[]" rows="2" class="form-control" placeholder="Describe the problem solved, architecture, and key features..." required></textarea>
          </div>
        </div>
      `;
      projContainer.appendChild(row);
    });
  }

  // 6. Add Skill Row
  const addSkillBtn = document.getElementById('btn-add-skill');
  const skillContainer = document.getElementById('skills-container');
  if (addSkillBtn && skillContainer) {
    addSkillBtn.addEventListener('click', function () {
      const row = document.createElement('div');
      row.className = 'dynamic-item-card py-2';
      row.innerHTML = `
        <div class="row g-2 align-items-center">
          <div class="col-md-5">
            <input type="text" name="skill_name[]" class="form-control form-control-sm" placeholder="Skill name (e.g. Python, MySQL, React)" required>
          </div>
          <div class="col-md-4">
            <select name="skill_category[]" class="form-select form-select-sm">
              <option value="programming">Programming Languages</option>
              <option value="database">Database Technologies</option>
              <option value="web">Web Technologies</option>
              <option value="other">Other Technical Skills</option>
            </select>
          </div>
          <div class="col-md-2">
            <select name="skill_proficiency[]" class="form-select form-select-sm">
              <option value="Beginner">Beginner</option>
              <option value="Intermediate" selected>Intermediate</option>
              <option value="Advanced">Advanced</option>
              <option value="Expert">Expert</option>
            </select>
          </div>
          <div class="col-md-1 text-end">
            <button type="button" class="btn-remove-item btn-remove-dynamic" title="Remove skill">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
        </div>
      `;
      skillContainer.appendChild(row);
    });
  }

  // 7. Add Certification Row
  const addCertBtn = document.getElementById('btn-add-certification');
  const certContainer = document.getElementById('certification-container');
  if (addCertBtn && certContainer) {
    addCertBtn.addEventListener('click', function () {
      const row = document.createElement('div');
      row.className = 'dynamic-item-card';
      row.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-primary"><i class="fa-solid fa-award me-1"></i> Certification</span>
          <button type="button" class="btn-remove-item btn-remove-dynamic" title="Remove certification">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        <div class="row g-3">
          <div class="col-md-5">
            <label class="form-label small fw-semibold">Certification Name *</label>
            <input type="text" name="cert_name[]" class="form-control" placeholder="e.g. AWS Certified Cloud Practitioner" required>
          </div>
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Issuing Organization *</label>
            <input type="text" name="cert_org[]" class="form-control" placeholder="e.g. Amazon Web Services" required>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Issue Year</label>
            <input type="text" name="cert_year[]" class="form-control" placeholder="e.g. 2024">
          </div>
        </div>
      `;
      certContainer.appendChild(row);
    });
  }
});
