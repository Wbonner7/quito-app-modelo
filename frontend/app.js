const API_BASE = "http://127.0.0.1:8000";

const advertiserTypeSelect = document.querySelector('#advertiser-form select[name="advertiser_type"]');
const metadataTextarea = document.querySelector('#advertiser-form textarea[name="metadata"]');
const plansSelect = document.querySelector('#advertiser-form select[name="plan_id"]');
const plansList = document.querySelector('#plans-list');
const plansButton = document.querySelector('#load-plans');

async function fetchJSON(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || response.statusText);
  }
  return response.json();
}

function renderPlans(plans) {
  plansList.innerHTML = '';
  plansSelect.innerHTML = '';
  plans.forEach((plan) => {
    const item = document.createElement('li');
    item.innerHTML = `<strong>${plan.name}</strong> — R$ ${plan.price}<br /><small>${plan.description}</small>`;
    plansList.appendChild(item);

    const option = document.createElement('option');
    option.value = plan.id;
    option.textContent = `${plan.name} (${plan.id})`;
    plansSelect.appendChild(option);
  });
}

async function loadPlans() {
  try {
    const plans = await fetchJSON('/plans/');
    renderPlans(plans);
  } catch (error) {
    plansList.innerHTML = `<li class="error">${error.message}</li>`;
  }
}

plansButton.addEventListener('click', () => {
  loadPlans();
});

const metadataTemplates = {
  broker: { creci: '' },
  agency: { cnpj: '' },
  developer: { cnpj: '', portfolio_url: '' },
};

advertiserTypeSelect.addEventListener('change', () => {
  const template = metadataTemplates[advertiserTypeSelect.value] || {};
  metadataTextarea.value = JSON.stringify(template, null, 2);
});

loadPlans();
advertiserTypeSelect.dispatchEvent(new Event('change'));

function parseMetadata(raw) {
  try {
    return JSON.parse(raw || '{}');
  } catch (error) {
    throw new Error('Metadados devem ser um JSON válido.');
  }
}

function handleFormSubmission(form, onSubmit, feedbackElement) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    feedbackElement.textContent = 'Processando…';
    try {
      const payload = onSubmit(new FormData(form));
      const data = await payload;
      feedbackElement.textContent = JSON.stringify(data, null, 2);
      form.reset();
      loadPlans();
      advertiserTypeSelect.dispatchEvent(new Event('change'));
    } catch (error) {
      feedbackElement.textContent = `Erro: ${error.message}`;
    }
  });
}

const advertiserFeedback = document.querySelector('#advertiser-feedback');
handleFormSubmission(
  document.querySelector('#advertiser-form'),
  async (formData) => {
    const metadata = parseMetadata(formData.get('metadata'));
    const body = {
      name: formData.get('name'),
      email: formData.get('email'),
      advertiser_type: formData.get('advertiser_type'),
      plan_id: formData.get('plan_id'),
      document: formData.get('document'),
      document_status: formData.get('document_status'),
      metadata,
    };
    return fetchJSON('/advertisers/', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },
  advertiserFeedback,
);

const propertyFeedback = document.querySelector('#property-feedback');
handleFormSubmission(
  document.querySelector('#property-form'),
  async (formData) => {
    const amenities = (formData.get('amenities') || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
    const body = {
      advertiser_id: formData.get('advertiser_id'),
      title: formData.get('title'),
      description: formData.get('description'),
      price: Number(formData.get('price')),
      address: formData.get('address'),
      bedrooms: Number(formData.get('bedrooms')),
      bathrooms: Number(formData.get('bathrooms')),
      area_m2: Number(formData.get('area_m2')),
      amenities,
    };
    return fetchJSON('/properties/', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },
  propertyFeedback,
);

const analyticsFeedback = document.querySelector('#analytics-feedback');
const registerViewButton = document.querySelector('#register-view');
const analyticsForm = document.querySelector('#analytics-form');

analyticsForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const propertyId = new FormData(analyticsForm).get('property_id');
  analyticsFeedback.textContent = 'Buscando…';
  registerViewButton.disabled = true;
  try {
    const analytics = await fetchJSON(`/analytics/properties/${propertyId}`);
    analyticsFeedback.textContent = JSON.stringify(analytics, null, 2);
    registerViewButton.disabled = false;
    registerViewButton.dataset.propertyId = propertyId;
  } catch (error) {
    analyticsFeedback.textContent = `Erro: ${error.message}`;
  }
});

registerViewButton.addEventListener('click', async () => {
  const propertyId = registerViewButton.dataset.propertyId;
  if (!propertyId) return;
  registerViewButton.disabled = true;
  try {
    const analytics = await fetchJSON(`/properties/${propertyId}/metrics/views`, {
      method: 'POST',
    });
    analyticsFeedback.textContent = JSON.stringify(analytics, null, 2);
  } catch (error) {
    analyticsFeedback.textContent = `Erro: ${error.message}`;
  } finally {
    registerViewButton.disabled = false;
  }
});
