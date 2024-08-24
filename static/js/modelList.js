// Function to fetch model list from server
async function fetchModelList() {
    try {
        const response = await fetch('/models/models');
        const data = await response.json();

        if (data.status === 'success') {
            return data.data;  // 返回模型列表数据
        } else {
            throw new Error(data.message || 'Failed to fetch model list');
        }
    } catch (error) {
        console.error('Error fetching model list:', error);
        return null;
    }
}

// Function to populate model types select element
function populateModelTypes(modelSelect, modelList) {
    modelSelect.innerHTML = '';
    modelList.forEach(item => {
        const option = document.createElement('option');
        option.value = item.category;
        option.textContent = item.category;
        modelSelect.appendChild(option);
    });
}

// Function to populate model names select element
function populateModelNames(modelNameSelect, modelList, modelType) {
    modelNameSelect.innerHTML = '';
    const selectedCategory = modelList.find(item => item.category === modelType);
    if (selectedCategory) {
        selectedCategory.models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.value;
            option.textContent = model.name;
            modelNameSelect.appendChild(option);
        });
    }
}

// Main function to initialize the model selection
async function initializeModelSelection() {
    const modelSelect = document.getElementById('modelSelect');
    const modelNameSelect = document.getElementById('modelNameSelect');

    if (!modelSelect || !modelNameSelect) {
        console.error("Couldn't find modelSelect or modelNameSelect elements");
        return;
    }

    const modelList = await fetchModelList();
    if (!modelList) {
        console.error('Failed to fetch model list');
        return;
    }

    populateModelTypes(modelSelect, modelList);
    populateModelNames(modelNameSelect, modelList, modelSelect.value);

    modelSelect.addEventListener('change', () => {
        populateModelNames(modelNameSelect, modelList, modelSelect.value);
    });
}

export { initializeModelSelection };