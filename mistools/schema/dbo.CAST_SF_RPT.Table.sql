DROP TABLE [dbo].[CAST_SF_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_SF_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_SF_RPT](
	[CAST_SF_RPT_ID] [bigint] NOT NULL,
	[CAST_SF_RPT_FLAG] [bit] NOT NULL,
	[CAST_SF_WORK_ID] [varchar](14) NULL,
	[CASTSF_COLLEGE_IDENTIFIER] [varchar](3) NULL,
	[CASTSF_TERM_IDENTIFIER] [varchar](3) NULL,
	[CASTSF_STU_NAME_PARTIAL] [varchar](3) NULL,
	[CASTSF_STU_IDENTIFIER] [varchar](9) NULL,
	[CASTSF_RECORD_NUMBER] [varchar](1) NULL,
	[CASTSF_APPLICANT_STATUS] [varchar](1) NULL,
	[CASTSF_TIME_PERIOD] [varchar](5) NULL,
	[CASTSF_DEPENDENCY_STATUS] [varchar](1) NULL,
	[CASTSF_HOUSEHOLD_SIZE] [varchar](2) NULL,
	[CASTSF_FAMILY_STATUS] [varchar](2) NULL,
	[CASTSF_INCOME_AGI_PARENT] [varchar](7) NULL,
	[CASTSF_INCOME_AGI_STUDENT] [varchar](7) NULL,
	[CASTSF_UNTAX_INC_PARENT] [varchar](8) NULL,
	[CASTSF_UNTAX_INC_STUDENT] [varchar](8) NULL,
	[CASTSF_AFDC_STATUS] [varchar](1) NULL,
	[CASTSF_UNMET_NEED] [varchar](5) NULL,
	[CASTSF_GROSS_FIN_NEED] [varchar](5) NULL,
	[CASTSF_EXP_FAMILY_CONTRIB] [varchar](6) NULL,
	[CASTSF_AWARD_TYPE_1] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_1] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_2] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_2] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_3] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_3] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_4] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_4] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_5] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_5] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_6] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_6] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_7] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_7] [varchar](5) NULL,
	[CASTSF_AWARD_TYPE_8] [varchar](2) NULL,
	[CASTSF_AMOUNT_RECEIVED_8] [varchar](5) NULL,
	[CASTSF_BUDGET_CATEGORY] [varchar](1) NULL,
	[CASTSF_BUDGET_AMT] [varchar](5) NULL,
	[CASTSF_STUDENT_ID] [varchar](10) NULL,
	[CASTSF_KEY_IDX] [varchar](20) NULL
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_SF_R__CAST___273BEF6F]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_SF_RPT] ADD  DEFAULT ((1)) FOR [CAST_SF_RPT_FLAG]
END
GO
