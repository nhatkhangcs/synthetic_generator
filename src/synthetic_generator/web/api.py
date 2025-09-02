"""
API endpoints for Synthetic Generator Web UI.
"""

import os
import tempfile
import json
import pandas as pd
import numpy as np
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime

# Import these functions directly to avoid circular imports
from ..schemas import DataSchema, ColumnSchema, DataType, DistributionType

api_bp = Blueprint("api", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"csv", "json", "xlsx", "parquet"}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "0.0.8",
        }
    )


@api_bp.route("/generate", methods=["POST"])
def generate_synthetic_data():
    """Generate synthetic data based on schema."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        schema_dict = data.get("schema")
        n_samples = data.get("n_samples", 1000)
        seed = data.get("seed")

        if not schema_dict:
            return jsonify({"error": "Schema is required"}), 400

        # Convert schema dict to DataSchema object
        schema = DataSchema.from_dict(schema_dict)

        # Import and generate data (avoid circular import)
        from ..generators.base import DataGenerator

        generator = DataGenerator(schema)
        result = generator.generate(n_samples, seed)

        # Convert to JSON-serializable format
        data_json = result.to_dict("records")
        
        # Ensure JSON serializable types (handle NaN values)
        def convert_numpy_types(obj):
            import numpy as np
            import math

            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating, float)):
                # Handle NaN values (both numpy and Python float)
                if np.isnan(obj) or math.isnan(obj):
                    return None
                return float(obj)
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, (np.ndarray,)):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            return obj

        # Convert all data to JSON-serializable format
        data_json = convert_numpy_types(data_json)

        return jsonify(
            {
                "success": True,
                "data": data_json,
                "shape": result.shape,
                "columns": list(result.columns),
                "sample_size": len(result),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/infer-schema", methods=["POST"])
def infer_data_schema():
    """Infer schema from uploaded data."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{file.filename.rsplit('.', 1)[1].lower()}"
        ) as tmp_file:
            file.save(tmp_file.name)

            # Read data based on file type
            if file.filename.endswith(".csv"):
                data = pd.read_csv(tmp_file.name)
            elif file.filename.endswith(".json"):
                data = pd.read_json(tmp_file.name)
            elif file.filename.endswith(".xlsx"):
                data = pd.read_excel(tmp_file.name)
            elif file.filename.endswith(".parquet"):
                data = pd.read_parquet(tmp_file.name)

            # Clean up temporary file
            os.unlink(tmp_file.name)

        # Infer schema (avoid circular import)
        sample_size = request.form.get("sample_size", type=int)
        from ..schemas.inference import infer_schema_from_data

        schema = infer_schema_from_data(data, sample_size)

        # Convert schema to dict
        schema_dict = schema.to_dict()

        return jsonify(
            {
                "success": True,
                "schema": schema_dict,
                "original_shape": data.shape,
                "columns": list(data.columns),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/templates", methods=["GET"])
def get_templates():
    """Get available templates."""
    try:
        templates = [
            {
                "name": "customer_data",
                "display_name": "Customer Data",
                "description": "Customer information with demographics and contact details",
                "category": "Business",
            },
            {
                "name": "medical_data",
                "display_name": "Medical Data",
                "description": "Patient data with health metrics and medical conditions",
                "category": "Healthcare",
            },
            {
                "name": "financial_data",
                "display_name": "Financial Data",
                "description": "Transaction data with amounts, categories, and temporal patterns",
                "category": "Finance",
            },
            {
                "name": "ecommerce_data",
                "display_name": "E-commerce Data",
                "description": "Order and product data with realistic business relationships",
                "category": "E-commerce",
            },
        ]

        return jsonify({"success": True, "templates": templates})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/templates/<template_name>", methods=["GET"])
def get_template(template_name):
    """Get specific template schema."""
    try:
        # Load template (avoid circular import)
        from ..schemas.templates import load_template_schema

        schema = load_template_schema(template_name)
        schema_dict = schema.to_dict()

        return jsonify(
            {"success": True, "template_name": template_name, "schema": schema_dict}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def validate_data_basic(data_df):
    """Perform basic data validation without requiring a schema."""
    import pandas as pd
    import numpy as np

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "statistics": {},
        "checks_passed": 0,
        "total_checks": 0,
        "check_details": [],
    }

    # Basic data integrity checks
    if data_df.empty:
        results["errors"].append("Data is empty")
        results["valid"] = False
        results["check_details"].append(
            {
                "type": "basic",
                "name": "Data integrity check",
                "status": "failed",
                "description": "Data contains no rows",
            }
        )
    else:
        results["check_details"].append(
            {
                "type": "basic",
                "name": "Data integrity check",
                "status": "passed",
                "description": f"Data contains {len(data_df)} rows",
            }
        )

    # Check for required columns (at least one column)
    if len(data_df.columns) == 0:
        results["errors"].append("Data has no columns")
        results["valid"] = False
        results["check_details"].append(
            {
                "type": "basic",
                "name": "Column existence check",
                "status": "failed",
                "description": "No columns found in data",
            }
        )
    else:
        results["check_details"].append(
            {
                "type": "basic",
                "name": "Column existence check",
                "status": "passed",
                "description": f"Found {len(data_df.columns)} columns",
            }
        )

    # Validate each column for basic data consistency
    for column_name in data_df.columns:
        col_data = data_df[column_name]
        col_stats = {
            "null_count": col_data.isnull().sum(),
            "unique_count": col_data.nunique(),
            "total_rows": len(col_data),
            "min_value": (
                col_data.min() if pd.api.types.is_numeric_dtype(col_data) else None
            ),
            "max_value": (
                col_data.max() if pd.api.types.is_numeric_dtype(col_data) else None
            ),
        }
        results["statistics"][column_name] = col_stats

        # Check for completely null columns
        if col_data.isnull().all():
            results["warnings"].append(f"Column {column_name}: All values are null")
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Null value check",
                    "status": "warning",
                    "description": "All values in this column are null",
                }
            )
        else:
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Null value check",
                    "status": "passed",
                    "description": f'Column has {col_stats["null_count"]} null values out of {col_stats["total_rows"]} total',
                }
            )

        # Check data type consistency
        if pd.api.types.is_bool_dtype(col_data):
            # Check for boolean consistency
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data type consistency",
                    "status": "passed",
                    "description": f"Column is consistently boolean type",
                }
            )
        elif (
            col_data.dtype == "object"
            and col_data.dropna().isin([True, False, "True", "False", 1, 0]).all()
        ):
            # Check for boolean-like values (True/False strings or actual booleans)
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data type consistency",
                    "status": "passed",
                    "description": f"Column contains boolean-like values (True/False)",
                }
            )
        elif pd.api.types.is_numeric_dtype(col_data):
            # Check for numeric consistency
            if col_data.dtype in ["int64", "float64", "int32", "float32"]:
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column_name,
                        "name": "Data type consistency",
                        "status": "passed",
                        "description": f"Column is consistently {col_data.dtype} type",
                    }
                )
            else:
                results["check_details"].append(
                    {
                        "type": "column",
                        "column": column_name,
                        "name": "Data type consistency",
                        "status": "warning",
                        "description": f"Column has mixed numeric types: {col_data.dtype}",
                    }
                )
        elif pd.api.types.is_string_dtype(col_data):
            # Check for string consistency
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data type consistency",
                    "status": "passed",
                    "description": f"Column is consistently string type",
                }
            )
        elif pd.api.types.is_datetime64_dtype(col_data):
            # Check for datetime consistency
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data type consistency",
                    "status": "passed",
                    "description": f"Column is consistently datetime type",
                }
            )
        else:
            # Mixed or unknown types
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data type consistency",
                    "status": "warning",
                    "description": f"Column has mixed or unknown types: {col_data.dtype}",
                }
            )

        # Check for potential data quality issues
        if col_data.nunique() == 1 and len(col_data) > 1:
            results["warnings"].append(
                f"Column {column_name}: All values are identical"
            )
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data variety check",
                    "status": "warning",
                    "description": "All values in this column are identical",
                }
            )
        else:
            results["check_details"].append(
                {
                    "type": "column",
                    "column": column_name,
                    "name": "Data variety check",
                    "status": "passed",
                    "description": f"Column has {col_data.nunique()} unique values",
                }
            )

    # Calculate checks passed and total checks
    total_checks = len(results["check_details"])
    checks_passed = len(
        [check for check in results["check_details"] if check["status"] == "passed"]
    )

    results["checks_passed"] = checks_passed
    results["total_checks"] = total_checks

    return results


@api_bp.route("/validate", methods=["POST"])
def validate_synthetic_data():
    """Validate generated data against schema."""
    try:
        data_df = None
        schema_dict = None

        # Support both JSON body and multipart file uploads
        if request.content_type and request.content_type.startswith("application/json"):
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            data_df = pd.DataFrame(data.get("data", []))
            schema_dict = data.get("schema")
        else:
            # Try multipart form: data_file (required), schema_file (optional)
            if "data_file" not in request.files:
                return jsonify({"error": "No data file uploaded"}), 400
            data_file = request.files["data_file"]
            if data_file.filename == "":
                return jsonify({"error": "No data file selected"}), 400
            # Save and read
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f".{data_file.filename.rsplit('.', 1)[1].lower()}"
            ) as tmp_file:
                data_file.save(tmp_file.name)
                if data_file.filename.endswith(".csv"):
                    data_df = pd.read_csv(tmp_file.name)
                elif data_file.filename.endswith(".json"):
                    data_df = pd.read_json(tmp_file.name)
                elif data_file.filename.endswith(".xlsx"):
                    data_df = pd.read_excel(tmp_file.name)
                elif data_file.filename.endswith(".parquet"):
                    data_df = pd.read_parquet(tmp_file.name)
                else:
                    os.unlink(tmp_file.name)
                    return jsonify({"error": "Unsupported data file type"}), 400
                os.unlink(tmp_file.name)

            if "schema_file" in request.files and request.files["schema_file"].filename:
                schema_file = request.files["schema_file"]
                schema_text = schema_file.read().decode("utf-8")
                schema_dict = json.loads(schema_text)

        if data_df is None:
            return jsonify({"error": "Failed to read data for validation"}), 400

        # Build schema: use provided schema if present; otherwise do basic validation
        if schema_dict:
            schema = DataSchema.from_dict(schema_dict)
            # Validate data against schema (avoid circular import)
            validation_results = schema.validate_data(data_df)
        else:
            # No schema provided - do basic data consistency validation
            validation_results = validate_data_basic(data_df)

        # Ensure JSON serializable types
        def convert_numpy_types(obj):
            import numpy as np

            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.bool_,)):
                return bool(obj)
            if isinstance(obj, (np.ndarray,)):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            return obj

        validation_serializable = convert_numpy_types(validation_results)

        return jsonify({"success": True, "validation": validation_serializable})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/export", methods=["POST"])
def export_generated_data():
    """Export generated data to various formats."""
    tmp_file_path = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        data_df = pd.DataFrame(data.get("data", []))
        export_format = data.get("format", "csv")
        filename = data.get(
            "filename", f'synthetic_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        )

        # Map logical format names to file extensions
        extension_map = {
            "csv": "csv",
            "json": "json",
            "excel": "xlsx",
            "parquet": "parquet",
        }
        file_ext = extension_map.get(export_format, export_format)

        # Create temporary file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}")
        tmp_file_path = tmp_file.name
        tmp_file.close()

        # Export data based on format
        if export_format == "csv":
            data_df.to_csv(tmp_file_path, index=False)
            mimetype = "text/csv"
        elif export_format == "json":
            data_df.to_json(tmp_file_path, orient="records", indent=2)
            mimetype = "application/json"
        elif export_format == "excel":
            # Try available Excel engines explicitly
            engine = None
            try:
                import openpyxl  # noqa: F401

                engine = "openpyxl"
            except ImportError:
                try:
                    import xlsxwriter  # noqa: F401

                    engine = "xlsxwriter"
                except ImportError:
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)
                    return (
                        jsonify(
                            {
                                "error": "Excel export requires 'openpyxl' or 'xlsxwriter'. Please install one of them."
                            }
                        ),
                        500,
                    )

            with pd.ExcelWriter(tmp_file_path, engine=engine) as writer:
                data_df.to_excel(writer, index=False, sheet_name="Sheet1")
            mimetype = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif export_format == "parquet":
            try:
                data_df.to_parquet(tmp_file_path, index=False)
            except Exception as e:
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                return (
                    jsonify(
                        {
                            "error": f"Parquet export failed: {str(e)}. Ensure 'pyarrow' or 'fastparquet' is installed."
                        }
                    ),
                    500,
                )
            mimetype = "application/octet-stream"
        else:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            return (
                jsonify({"error": f"Unsupported export format: {export_format}"}),
                400,
            )

        # Send file and ensure cleanup
        response = send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=f"{filename}.{file_ext}",
            mimetype=mimetype,
        )

        # Add cleanup callback
        @response.call_on_close
        def cleanup():
            try:
                if tmp_file_path and os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

        return response

    except Exception as e:
        # Clean up temporary file on error
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except Exception:
                pass
        return jsonify({"error": str(e)}), 500


@api_bp.route("/statistics", methods=["POST"])
def get_data_statistics():
    """Get statistical analysis of generated data."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        data_df = pd.DataFrame(data.get("data", []))

        # Calculate basic statistics
        stats = {
            "shape": data_df.shape,
            "columns": list(data_df.columns),
            "dtypes": data_df.dtypes.astype(str).to_dict(),
            "missing_values": data_df.isnull().sum().to_dict(),
            "numeric_stats": {},
            "categorical_stats": {},
        }

        # Numeric statistics
        numeric_cols = data_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats["numeric_stats"] = data_df[numeric_cols].describe().to_dict()

        # Categorical statistics
        categorical_cols = data_df.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            stats["categorical_stats"][col] = {
                "unique_count": data_df[col].nunique(),
                "top_values": data_df[col].value_counts().head(5).to_dict(),
            }

        return jsonify({"success": True, "statistics": stats})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/data-types", methods=["GET"])
def get_data_types():
    """Get available data types."""
    try:
        data_types = [
            {"value": "INTEGER", "label": "Integer", "category": "Numeric"},
            {"value": "FLOAT", "label": "Float", "category": "Numeric"},
            {"value": "STRING", "label": "String", "category": "Text"},
            {"value": "EMAIL", "label": "Email", "category": "Text"},
            {"value": "PHONE", "label": "Phone", "category": "Text"},
            {"value": "ADDRESS", "label": "Address", "category": "Text"},
            {"value": "NAME", "label": "Name", "category": "Text"},
            {"value": "CATEGORICAL", "label": "Categorical", "category": "Categorical"},
            {"value": "BOOLEAN", "label": "Boolean", "category": "Categorical"},
            {"value": "DATE", "label": "Date", "category": "Temporal"},
            {"value": "DATETIME", "label": "DateTime", "category": "Temporal"},
        ]

        return jsonify({"success": True, "data_types": data_types})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/distributions", methods=["GET"])
def get_distributions():
    """Get available distributions."""
    try:
        distributions = [
            {"value": "NORMAL", "label": "Normal", "category": "Continuous"},
            {"value": "UNIFORM", "label": "Uniform", "category": "Continuous"},
            {"value": "EXPONENTIAL", "label": "Exponential", "category": "Continuous"},
            {"value": "GAMMA", "label": "Gamma", "category": "Continuous"},
            {"value": "BETA", "label": "Beta", "category": "Continuous"},
            {"value": "WEIBULL", "label": "Weibull", "category": "Continuous"},
            {"value": "POISSON", "label": "Poisson", "category": "Discrete"},
            {"value": "BINOMIAL", "label": "Binomial", "category": "Discrete"},
            {"value": "GEOMETRIC", "label": "Geometric", "category": "Discrete"},
            {"value": "CATEGORICAL", "label": "Categorical", "category": "Categorical"},
            {"value": "CONSTANT", "label": "Constant", "category": "Special"},
        ]

        return jsonify({"success": True, "distributions": distributions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
