test:
	GHOSTDB_DB_DSN='mysql://vis:vis@localhost:3306/vis_test' python -m pytest  \
		--pylama \
		--ignore=./ghostdb/alembic --ignore=create_records.py \
		-s \
		ghostdb/


deps-compile:
	for name in common ci dev; do \
		pip-compile requirements/$$name.in; \
	done
