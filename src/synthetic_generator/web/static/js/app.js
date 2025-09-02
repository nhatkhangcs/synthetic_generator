/**
 * Main JavaScript file for Synthetic Generator Web UI
 */

// Global variables
let currentData = null;
let currentSchema = null;

// Utility functions
const utils = {
    showNotification: function(message, type = 'info') {
        const alertClass = type === 'error' ? 'alert-danger' : 
                          type === 'success' ? 'alert-success' : 
                          type === 'warning' ? 'alert-warning' : 'alert-info';
        
        const alert = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Insert at the top of the main container
        const container = document.querySelector('main');
        container.insertAdjacentHTML('afterbegin', alert);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    },
    
    formatNumber: function(num) {
        return new Intl.NumberFormat().format(num);
    },
    
    formatBytes: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    downloadFile: function(data, filename, type) {
        const blob = new Blob([data], { type: type });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
};

// API functions
const api = {
    baseUrl: '',
    
    async request(endpoint, options = {}) {
        const url = this.baseUrl + endpoint;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async upload(endpoint, formData) {
        return this.request(endpoint, {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set content-type for FormData
        });
    }
};

// Data generation functions
const dataGenerator = {
    async generate(schema, options = {}) {
        try {
            const response = await api.post('/api/generate', {
                schema: schema,
                n_samples: options.n_samples || 1000,
                seed: options.seed || null
            });
            
            currentData = response.data;
            currentSchema = schema;
            
            return response;
        } catch (error) {
            throw new Error(`Failed to generate data: ${error.message}`);
        }
    },
    
    async validate(data, schema) {
        try {
            const response = await api.post('/api/validate', {
                data: data,
                schema: schema
            });
            
            return response;
        } catch (error) {
            throw new Error(`Failed to validate data: ${error.message}`);
        }
    },
    
    async getStatistics(data) {
        try {
            const response = await api.post('/api/statistics', {
                data: data
            });
            
            return response;
        } catch (error) {
            throw new Error(`Failed to get statistics: ${error.message}`);
        }
    },
    
    async export(data, format, filename) {
        try {
            const response = await api.post('/api/export', {
                data: data,
                format: format,
                filename: filename
            });
            
            return response;
        } catch (error) {
            throw new Error(`Failed to export data: ${error.message}`);
        }
    }
};

// Template management
const templateManager = {
    async getTemplates() {
        try {
            const response = await api.get('/api/templates');
            return response.templates;
        } catch (error) {
            throw new Error(`Failed to load templates: ${error.message}`);
        }
    },
    
    async getTemplate(name) {
        try {
            const response = await api.get(`/api/templates/${name}`);
            return response.schema;
        } catch (error) {
            throw new Error(`Failed to load template: ${error.message}`);
        }
    }
};

// Schema inference
const schemaInference = {
    async infer(file, options = {}) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            if (options.sample_size) {
                formData.append('sample_size', options.sample_size);
            }
            
            const response = await api.upload('/api/infer-schema', formData);
            return response.schema;
        } catch (error) {
            throw new Error(`Failed to infer schema: ${error.message}`);
        }
    }
};

// UI components
const ui = {
    showLoading: function(element, message = 'Loading...') {
        element.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">${message}</p>
            </div>
        `;
    },
    
    hideLoading: function(element) {
        element.innerHTML = '';
    },
    
    showError: function(element, message) {
        element.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    },
    
    showSuccess: function(element, message) {
        element.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>
                ${message}
            </div>
        `;
    },
    
    createDataTable: function(data, columns, maxRows = 10) {
        let html = `
            <div class="table-responsive">
                <table class="table table-sm table-striped">
                    <thead>
                        <tr>
                            ${columns.map(col => `<th>${col}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        const rowsToShow = data.slice(0, maxRows);
        rowsToShow.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                const value = row[col];
                html += `<td>${value !== null && value !== undefined ? value : ''}</td>`;
            });
            html += '</tr>';
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        if (data.length > maxRows) {
            html += `<p class="text-muted">Showing first ${maxRows} rows of ${data.length} total rows</p>`;
        }
        
        return html;
    },
    
    createStatisticsPanel: function(stats) {
        let html = `
            <div class="row">
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-primary">${stats.shape[0]}</h4>
                        <small class="text-muted">Rows</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="text-center">
                        <h4 class="text-primary">${stats.shape[1]}</h4>
                        <small class="text-muted">Columns</small>
                    </div>
                </div>
            </div>
        `;
        
        if (Object.keys(stats.numeric_stats).length > 0) {
            html += '<hr><h6>Numeric Statistics</h6>';
            Object.keys(stats.numeric_stats).forEach(col => {
                const colStats = stats.numeric_stats[col];
                html += `
                    <div class="mb-2">
                        <small class="text-muted fw-bold">${col}</small>
                        <div class="row">
                            <div class="col-6">
                                <small>Mean: ${colStats.mean?.toFixed(2) || 'N/A'}</small>
                            </div>
                            <div class="col-6">
                                <small>Std: ${colStats.std?.toFixed(2) || 'N/A'}</small>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        if (Object.keys(stats.categorical_stats).length > 0) {
            html += '<hr><h6>Categorical Statistics</h6>';
            Object.keys(stats.categorical_stats).forEach(col => {
                const colStats = stats.categorical_stats[col];
                html += `
                    <div class="mb-2">
                        <small class="text-muted fw-bold">${col}</small>
                        <div>Unique values: ${colStats.unique_count}</div>
                    </div>
                `;
            });
        }
        
        return html;
    }
};

// File handling
const fileHandler = {
    setupDragAndDrop: function(dropZone, callback) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
        
        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                callback(files[0]);
            }
        });
        
        dropZone.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.csv,.json,.xlsx,.parquet';
            input.onchange = (e) => {
                if (e.target.files.length > 0) {
                    callback(e.target.files[0]);
                }
            };
            input.click();
        });
    },
    
    validateFile: function(file) {
        const allowedTypes = ['text/csv', 'application/json', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
        const allowedExtensions = ['.csv', '.json', '.xlsx', '.parquet'];
        
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
            throw new Error('Invalid file type. Please upload CSV, JSON, Excel, or Parquet files.');
        }
        
        if (file.size > 16 * 1024 * 1024) { // 16MB limit
            throw new Error('File size too large. Please upload files smaller than 16MB.');
        }
        
        return true;
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Synthetic Generator Web UI initialized');
    
    // Check API health
    api.get('/api/health')
        .then(response => {
            console.log('API Status:', response.status);
        })
        .catch(error => {
            console.error('API Health Check Failed:', error);
            utils.showNotification('API connection failed. Please check if the server is running.', 'error');
        });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Export for use in other scripts
window.SyntheticGenerator = {
    utils,
    api,
    dataGenerator,
    templateManager,
    schemaInference,
    ui,
    fileHandler
};
