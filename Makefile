include *.mk


test:
	PYTHONPATH=${GHOSTDB_PATH} \
	GHOSTDB_DB_DSN=${GHOSTDB_DB_DSN_FOR_TEST} \
		python -m pytest  \
			--pylama \
			--bandit \
			--ignore=./ghostdb/alembic --ignore=create_records.py \
			-s \
			ghostdb/


deps-compile:
	for name in common ci dev; do \
		pip-compile --no-emit-index-url requirements/$$name.in; \
	done
