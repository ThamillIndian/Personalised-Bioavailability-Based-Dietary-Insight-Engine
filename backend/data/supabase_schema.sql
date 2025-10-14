-- ================================================
-- Smart Recipe Generator Database Schema
-- Supabase PostgreSQL Schema
-- ================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================
-- RECIPES TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS recipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    cuisine_type VARCHAR(100),
    difficulty VARCHAR(50) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    prep_time INTEGER NOT NULL CHECK (prep_time > 0), -- minutes
    cook_time INTEGER NOT NULL CHECK (cook_time > 0), -- minutes
    servings INTEGER DEFAULT 4 CHECK (servings > 0),
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for common queries
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine_type);
CREATE INDEX idx_recipes_difficulty ON recipes(difficulty);
CREATE INDEX idx_recipes_total_time ON recipes((prep_time + cook_time));

-- ================================================
-- RECIPE INGREDIENTS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    is_critical BOOLEAN DEFAULT FALSE,
    category VARCHAR(100), -- protein, vegetable, grain, dairy, spice, other
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for ingredient matching
CREATE INDEX idx_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_ingredients_name ON recipe_ingredients(LOWER(ingredient_name));
CREATE INDEX idx_ingredients_category ON recipe_ingredients(category);

-- ================================================
-- RECIPE INSTRUCTIONS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS recipe_instructions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    duration_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(recipe_id, step_number)
);

-- Index for ordering
CREATE INDEX idx_instructions_recipe ON recipe_instructions(recipe_id, step_number);

-- ================================================
-- RECIPE NUTRITION TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS recipe_nutrition (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipe_id UUID NOT NULL UNIQUE REFERENCES recipes(id) ON DELETE CASCADE,
    calories INTEGER,
    protein DECIMAL(10, 2),
    carbs DECIMAL(10, 2),
    fat DECIMAL(10, 2),
    fiber DECIMAL(10, 2),
    sugar DECIMAL(10, 2),
    sodium DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for nutrition filtering
CREATE INDEX idx_nutrition_recipe ON recipe_nutrition(recipe_id);
CREATE INDEX idx_nutrition_calories ON recipe_nutrition(calories);
CREATE INDEX idx_nutrition_protein ON recipe_nutrition(protein);

-- ================================================
-- DIETARY TAGS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS recipe_dietary_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(recipe_id, tag)
);

-- Index for dietary filtering
CREATE INDEX idx_dietary_tags_recipe ON recipe_dietary_tags(recipe_id);
CREATE INDEX idx_dietary_tags_tag ON recipe_dietary_tags(LOWER(tag));

-- ================================================
-- USER PREFERENCES TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE, -- From auth or session
    dietary_restrictions TEXT[], -- Array of restrictions
    favorite_cuisines TEXT[], -- Array of favorite cuisines
    disliked_ingredients TEXT[], -- Array of disliked ingredients
    cooking_skill_level VARCHAR(50) DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ================================================
-- FAVORITES TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, recipe_id)
);

-- Indexes for favorites
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_recipe ON favorites(recipe_id);
CREATE INDEX idx_favorites_created ON favorites(created_at DESC);

-- ================================================
-- RATINGS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, recipe_id)
);

-- Indexes for ratings
CREATE INDEX idx_ratings_user ON ratings(user_id);
CREATE INDEX idx_ratings_recipe ON ratings(recipe_id);
CREATE INDEX idx_ratings_rating ON ratings(rating);

-- ================================================
-- VIEWS FOR COMMON QUERIES
-- ================================================

-- View: Recipes with average ratings
CREATE OR REPLACE VIEW recipes_with_ratings AS
SELECT 
    r.*,
    COALESCE(AVG(rat.rating), 0) as average_rating,
    COUNT(rat.id) as total_ratings
FROM recipes r
LEFT JOIN ratings rat ON r.id = rat.recipe_id
GROUP BY r.id;

-- View: Popular recipes (most favorited)
CREATE OR REPLACE VIEW popular_recipes AS
SELECT 
    r.*,
    COUNT(f.id) as favorite_count
FROM recipes r
LEFT JOIN favorites f ON r.id = f.recipe_id
GROUP BY r.id
ORDER BY favorite_count DESC;

-- ================================================
-- FUNCTIONS
-- ================================================

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update updated_at for recipes
CREATE TRIGGER update_recipes_updated_at
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Auto-update updated_at for ratings
CREATE TRIGGER update_ratings_updated_at
    BEFORE UPDATE ON ratings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- ROW LEVEL SECURITY (Optional - enable if using Supabase Auth)
-- ================================================

-- Enable RLS on tables
-- ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE ratings ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Policies (example - customize based on auth strategy)
-- CREATE POLICY "Users can view all recipes" ON recipes
--     FOR SELECT USING (true);

-- CREATE POLICY "Users can manage their own favorites" ON favorites
--     FOR ALL USING (auth.uid() = user_id);

-- CREATE POLICY "Users can manage their own ratings" ON ratings
--     FOR ALL USING (auth.uid() = user_id);

-- ================================================
-- SEED DATA INSERTION HELPER
-- ================================================

-- Function to insert complete recipe with all related data
CREATE OR REPLACE FUNCTION insert_complete_recipe(
    p_title VARCHAR,
    p_description TEXT,
    p_cuisine_type VARCHAR,
    p_difficulty VARCHAR,
    p_prep_time INTEGER,
    p_cook_time INTEGER,
    p_servings INTEGER,
    p_image_url TEXT,
    p_ingredients JSONB,
    p_instructions JSONB,
    p_dietary_tags TEXT[],
    p_nutrition JSONB
) RETURNS UUID AS $$
DECLARE
    v_recipe_id UUID;
    v_ingredient JSONB;
    v_instruction JSONB;
    v_tag TEXT;
BEGIN
    -- Insert recipe
    INSERT INTO recipes (title, description, cuisine_type, difficulty, prep_time, cook_time, servings, image_url)
    VALUES (p_title, p_description, p_cuisine_type, p_difficulty, p_prep_time, p_cook_time, p_servings, p_image_url)
    RETURNING id INTO v_recipe_id;
    
    -- Insert ingredients
    FOR v_ingredient IN SELECT * FROM jsonb_array_elements(p_ingredients)
    LOOP
        INSERT INTO recipe_ingredients (recipe_id, ingredient_name, quantity, unit, is_critical, category)
        VALUES (
            v_recipe_id,
            v_ingredient->>'name',
            (v_ingredient->>'quantity')::DECIMAL,
            v_ingredient->>'unit',
            (v_ingredient->>'is_critical')::BOOLEAN,
            v_ingredient->>'category'
        );
    END LOOP;
    
    -- Insert instructions
    FOR v_instruction IN SELECT * FROM jsonb_array_elements(p_instructions)
    LOOP
        INSERT INTO recipe_instructions (recipe_id, step_number, instruction, duration_minutes)
        VALUES (
            v_recipe_id,
            (v_instruction->>'step_number')::INTEGER,
            v_instruction->>'instruction',
            (v_instruction->>'duration_minutes')::INTEGER
        );
    END LOOP;
    
    -- Insert dietary tags
    FOREACH v_tag IN ARRAY p_dietary_tags
    LOOP
        INSERT INTO recipe_dietary_tags (recipe_id, tag)
        VALUES (v_recipe_id, v_tag);
    END LOOP;
    
    -- Insert nutrition
    IF p_nutrition IS NOT NULL THEN
        INSERT INTO recipe_nutrition (recipe_id, calories, protein, carbs, fat, fiber, sugar, sodium)
        VALUES (
            v_recipe_id,
            (p_nutrition->>'calories')::INTEGER,
            (p_nutrition->>'protein')::DECIMAL,
            (p_nutrition->>'carbs')::DECIMAL,
            (p_nutrition->>'fat')::DECIMAL,
            (p_nutrition->>'fiber')::DECIMAL,
            (p_nutrition->>'sugar')::DECIMAL,
            (p_nutrition->>'sodium')::DECIMAL
        );
    END IF;
    
    RETURN v_recipe_id;
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- GRANT PERMISSIONS (adjust based on your setup)
-- ================================================

-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

