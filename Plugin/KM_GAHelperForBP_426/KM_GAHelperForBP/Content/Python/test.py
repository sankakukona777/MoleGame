import unreal
import shutil
import sys
import os
import subprocess
data = unreal.find_asset("/Game/KM_Attribute/AttributeTable")
class_names = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "ClassName")
property_names = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "PropertyName")
min_clamp_type = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MinClampType")
min_clamp_value = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MinClampValue")
min_clamp_property = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MinClampProperty")
max_clamp_type = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MaxClampType")
max_clamp_value = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MaxClampValue")
max_clamp_property = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "MaxClampProperty")
initial_value = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(data, "InitialValue")

header_dir = unreal.SystemLibrary.get_project_directory() + "Source/" + unreal.SystemLibrary.get_game_name() + "/Public/KM_GAAttributes/"
source_dir = unreal.SystemLibrary.get_project_directory() + "Source/" + unreal.SystemLibrary.get_game_name() + "/Private/KM_GAAttributes/"
macro_header_path = unreal.SystemLibrary.get_project_directory() + "Source/" + unreal.SystemLibrary.get_game_name() + "/Public/KM_AttributeSetMacros.h"
if os.path.exists(header_dir):
	shutil.rmtree(header_dir)
if os.path.exists(source_dir):
	shutil.rmtree(source_dir)

macro_header_content = """
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"

#define KM_GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
	static FGameplayAttribute Get##PropertyName##Attribute() \
	{ \
		static FProperty* Prop = FindFieldChecked<FProperty>(ClassName::StaticClass(), GET_MEMBER_NAME_CHECKED(ClassName, PropertyName)); \
		return Prop; \
	}

#define KM_GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
	FORCEINLINE float Get##PropertyName() const \
	{ \
		return PropertyName.GetCurrentValue(); \
	}

#define KM_GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
	FORCEINLINE void Set##PropertyName(float NewVal) \
	{ \
		UAbilitySystemComponent* AbilityComp = GetTargetComponent(); \
		if (ensure(AbilityComp)) \
		{ \
			AbilityComp->SetNumericAttributeBase(Get##PropertyName##Attribute(), NewVal); \
		}; \
	}

#define KM_GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName) \
	FORCEINLINE void Init##PropertyName(float NewVal) \
	{ \
		PropertyName.SetBaseValue(NewVal); \
		PropertyName.SetCurrentValue(NewVal); \
	}

#define KM_ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \
	KM_GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
	KM_GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
	KM_GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
	KM_GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)
"""

macro_file = open(macro_header_path, "w")
macro_file.write(macro_header_content)
macro_file.close()


# ヘッダー
pre_header_content = """
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "AttributeSet.h"
#include "AbilitySystemComponent.h"
#include "AbilitySystemGlobals.h"
#include "KM_AttributeSetMacros.h"
#include "{}.generated.h"
/**
 * 
 */
UCLASS()
class {}_API U{} : public UAttributeSet
{{
	GENERATED_BODY()
public:
	virtual void PostGameplayEffectExecute(const struct FGameplayEffectModCallbackData& Data);
	virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const;
	UAbilitySystemComponent* GetTargetComponent() {{ if (mTargetComponent != nullptr) {{ return mTargetComponent; }} mTargetComponent = UAbilitySystemGlobals::GetAbilitySystemComponentFromActor(GetOwningActor(), true); return mTargetComponent; }}
"""

property_header_content = """
	UPROPERTY(Category = "GPAAttributes", EditAnywhere, BlueprintReadWrite, ReplicatedUsing="OnRep_{}")
	FGameplayAttributeData {}{{ {}f }};
	KM_ATTRIBUTE_ACCESSORS(U{}, {});
	UFUNCTION()
	virtual void OnRep_{}(const FGameplayAttributeData& OldValue);
"""
post_header_content = """
private:
	UAbilitySystemComponent* mTargetComponent{ nullptr };
};
"""


# クラス分ループを回す
class_names_unique = set(class_names)
for class_index, class_name in enumerate(class_names_unique):
	added_property = []
	merged = pre_header_content.format(class_name, unreal.SystemLibrary.get_game_name().upper(), class_name)
	for index, element in enumerate(class_names):
		if(element != class_name):
			continue
		if(added_property.count(property_names[index]) > 0):
			continue
		added_property.append(property_names[index])
		p_content = property_header_content.format(property_names[index], property_names[index], initial_value[index], class_name, property_names[index], property_names[index])
		merged = merged + p_content
	merged = merged + post_header_content
	os.makedirs(header_dir, exist_ok=True)
	f = open(header_dir + class_name + ".h", "w")
	f.write(merged)
	f.close()


# cpp部分
effect_execute_content = """
	if (Data.EvaluatedData.Attribute == Get{prop}Attribute()) {{
		Set{prop}(FMath::Clamp(Get{prop}(), {min_value}, {max_value}));
	}}
"""

replicated_props_content = """
	DOREPLIFETIME_CONDITION_NOTIFY(U{class_name}, {prop}, COND_None, REPNOTIFY_Always);
"""

onrep_content = """
void U{class_name}::OnRep_{prop}(const FGameplayAttributeData& oldValue)
{{
	static FProperty* ThisProperty = FindFieldChecked<FProperty>(U{class_name}::StaticClass(), GET_MEMBER_NAME_CHECKED(U{class_name}, {prop})); 
	GetTargetComponent()->SetBaseAttributeValueFromReplication(FGameplayAttribute(ThisProperty), {prop}, oldValue); 
}}
"""

source_content = """
#include "KM_GAAttributes/{class_name}.h"
#include "GameplayEffect.h"
#include "GameplayEffectExtension.h"
#include "Net/UnrealNetwork.h"

void U{class_name}::PostGameplayEffectExecute(const struct FGameplayEffectModCallbackData& Data)
{{
	UAttributeSet::PostGameplayEffectExecute(Data);
	{e}
}}


void U{class_name}::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{{
	Super::GetLifetimeReplicatedProps(OutLifetimeProps);
	{r}
}}

{on}

"""

class_names_unique = set(class_names)
for class_index, class_name in enumerate(class_names_unique):
	added_property = []
	e_content = ""
	rep_prop_content = ""
	o_content = ""
	for index, element in enumerate(class_names):
		if(element != class_name):
			continue
		if(added_property.count(property_names[index]) > 0):
			continue
		added_property.append(property_names[index])
		min_value = "-999999.f"
		max_value = "999999.f"
		if min_clamp_type[index] == "Value":
			min_value = min_clamp_value[index] + "f"
		if min_clamp_type[index] == "Property":
			min_value = "Get" + min_clamp_property[index] + "()"
		if max_clamp_type[index] == "Value":
			max_value = max_clamp_value[index] + "f"
		if max_clamp_type[index] == "Property":
			max_value = "Get" + max_clamp_property[index] + "()"
		if min_clamp_type[index] != "None":
			e_content = e_content + effect_execute_content.format(prop=property_names[index], min_value=min_value, max_value=max_value)
		rep_prop_content = rep_prop_content + replicated_props_content.format(class_name=class_name, prop=property_names[index])
		o_content = o_content + onrep_content.format(class_name=class_name, prop=property_names[index])
		
	merged = source_content.format(e=e_content, r=rep_prop_content, on=o_content, class_name=class_name)
	os.makedirs(source_dir, exist_ok=True)
	f = open(source_dir + class_name + ".cpp", "w")
	f.write(merged)
	f.close()



build_tool = unreal.Paths.engine_dir() + "/Binaries/DotNET/UnrealBuildTool.exe"
if os.path.exists(build_tool) == False:
	build_tool = unreal.Paths.engine_dir() + "/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.exe"

process_string = build_tool + " -projectfiles -project=" + unreal.Paths.get_project_file_path() + " -game -rocket -progress"
subprocess.call(process_string)
